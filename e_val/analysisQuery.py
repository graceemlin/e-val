import json
import sgfmill
import sgfmill.common
import os.path
class AnalysisQuery:

    #{
    #     "id": "foo",
    #     "initialStones": [
    #         ["B", "Q4"],
    #         ["B", "C4"]
    #     ],
    #     "moves": [
    #         ["W", "P5"],
    #         ["B", "P6"]
    #     ],
    #     "rules": "tromp-taylor",
    #     "komi": 7.5,
    #     "boardXSize": 19,
    #     "boardYSize": 19,
    #     "analyzeTurns": [0, 1, 2]
    # }
    def __init__(self, id, game, board, basefile):
        self.id = id
        self.game = game
        self.board = board
        self.initialStones = game.setup
        self.moves = game.moves
        self.rules = game.rules
        self.komi = game.metadata.komi
        self.boardXSize = game.metadata.size
        self.boardYSize = game.metadata.size
        self.basefile = basefile
        self.analyzeTurns = []
        self.result = None

    def setResult(self, data):
        self.result = data

    def analyseAll(self):
        self.analyzeTurns = range(len(self.moves))

    def analyseTurn(self, turn):
        self.analyzeTurns.append(turn)

    def formatToQuery(self, stones):
        return [["B" if s[0]==1 else "W", f"({self.board.loc_x(s[1])},{self.board.loc_y(s[1])})"] for s in stones]

    def toJson(self):
        return json.dumps(self.toDict())

    def toDict(self):
        return {
            "id": self.id,
            "initialStones": self.formatToQuery(self.initialStones),
            "moves": self.formatToQuery(self.moves),
            "rules": self.rules,
            "komi": self.komi,
            "boardXSize": 19,
            "boardYSize": 19,
            "analyzeTurns": self.analyzeTurns
        }

    def hasResult(self):
        return self.result

    def printResult(self):
        print("Result")
        print(self.result["rootInfo"])
        print("Moves")
        for info in self.result["moveInfos"]:
            print(info)

    def outputToAnki(self, outdir, truncate):
        ANKI_HEADER = b"#separator:tab\n#html:true\n#tags column:2\n"
        with open(os.path.join(outdir,self.id+f"_deck.txt"), "wb") as d:
            d.write(ANKI_HEADER)
            for sgf in self.generateSGFs(one_per_variation=True, truncate=truncate):
                d.write(sgf)

    def generateSGFs(self, one_per_variation=False, truncate=False):
        with open(self.basefile, "r") as f:
            export_game = sgfmill.sgf.Sgf_game.from_string(f.read())
        result = []
        main_sequence = export_game.get_main_sequence()
        last_move = self.analyzeTurns[0] #TODO: this will only work as long as every query only queries a single move or queries in descending order
        last_node = main_sequence[last_move]
        if truncate:
            b_moves, w_moves, _ = export_game.get_root().get_setup_stones()
            b_moves = list(b_moves)
            w_moves = list(w_moves)
            c_node = main_sequence[0]
            while c_node != last_node:
                c,m = c_node.get_move()
                if c == 'b':
                    if m:
                        b_moves.append(m)
                else:
                    if m:
                        w_moves.append(m)
                c_node = c_node[0]
            export_game.get_root().set_setup_stones(b_moves, w_moves)
            for c in export_game.get_root():
                c.delete()
            last_node.reparent(export_game.get_root())
        #Truncate game to move at the end of analysis
        for child_node in last_node:
            child_node.delete()
        #Add marker to last move
        last_node.set("CR", [last_node.get_move()[1]])
        prior = self.result["rootInfo"]
        last_node.add_comment_text(f"WinRate: {prior['winrate']}, Points Lead: {prior['scoreLead']}")
        if not one_per_variation:
            #Append variations to move
            for moveInfo in self.result["moveInfos"]:
                toPlay = sgfmill.common.opponent_of(last_node.get_move()[0])
                variation_node = last_node.new_child()
                variation_node.add_comment_text(f"WinRate: {moveInfo['winrate']}, Points Lead: {moveInfo['scoreLead']}\nWinRate Diff: {moveInfo['winrate']-prior['winrate']}, Points Diff: {moveInfo['scoreLead']-prior['scoreLead']}")
                for m in moveInfo['pv']:
                    variation_node.set_move(toPlay, sgfmill.common.move_from_vertex(m, self.boardXSize))
                    toPlay = sgfmill.common.opponent_of(toPlay)
                    variation_node = variation_node.new_child()
            result = [export_game.serialise()]
        else:
            for moveInfo in self.result["moveInfos"]:
                toPlay = sgfmill.common.opponent_of(last_node.get_move()[0])
                variation_base = last_node.new_child()
                variation_base.add_comment_text(f"WinRate: {moveInfo['winrate']}, Points Lead: {moveInfo['scoreLead']}\nWinRate Diff: {moveInfo['winrate']-prior['winrate']}, Points Diff: {moveInfo['scoreLead']-prior['scoreLead']}")
                variation_node = variation_base
                for m in moveInfo['pv']:
                    variation_node.set_move(toPlay, sgfmill.common.move_from_vertex(m, self.boardXSize))
                    toPlay = sgfmill.common.opponent_of(toPlay)
                    variation_node = variation_node.new_child()
                data = export_game.serialise()
                data = data.replace(b"\n", b"")+b"\n" #remove newlines from sgf
                result.append(data)
                variation_base.delete()
        return result

    def outputToSGF(self, outdir, truncate=False):
        with open(os.path.join(outdir,self.id), "wb") as f:
            f.write(self.generateSGFs(one_per_variation=False, truncate=truncate)[0])