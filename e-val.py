import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"KataGo/python"))
from e_val import *
from data import load_sgf_moves_exn
from board import Board
from e_val import AnalysisQuery
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import tqdm

if __name__ == "__main__":
    argparser = ArgumentParser(prog="E-Val", description="Generates SGFs with variations from base SGF and list of moves to generate for", formatter_class=ArgumentDefaultsHelpFormatter)
    argparser.add_argument("-r", "--rules", choices=["japanese", "chinese", "chinese-ogs", "chinese-kgs", "tromp-taylor", "korean", "stone-scoring", "aga", "bga"], default="japanese")
    argparser.add_argument("-k", "--katago", help="Path to katago executable", default="./katago_bin/katago")
    argparser.add_argument("-a", "--analysis-config", help="Path to analysis config file for katago", default="./katago_bin/analysis_example.cfg")
    argparser.add_argument("-m", "--model", help="Path to katago model to use", default=None)
    argparser.add_argument("-o", "--outDir", help="Directory to write generated sgf files to", default=".")
    argparser.add_argument("-v", "--anki", help="Output the variations as an anki deck", default=False, action='store_true')
    argparser.add_argument("sgf_file", help="SGF file to analyze")
    argparser.add_argument("move", type=int, nargs='+', help="One or more move numbers to analyse, note that in handicap games the handicap stones might not be considered a move")

    args = argparser.parse_args()
    try:
        sgf_basename = os.path.basename(args.sgf_file)[:args.sgf_file.rindex('.')]
    except Exception:
        sgf_basename = os.path.basename(args.sgf_file)
    metadata, stones, moves, rules = load_sgf_moves_exn(args.sgf_file)
    board = Board(metadata.size,None)
    rules = args.rules
    game = Game(metadata,stones,moves,rules)
    engine = AnalysisEngine(args.katago,args.analysis_config, args.model)
    for m in tqdm.tqdm(args.move):
        query = AnalysisQuery(sgf_basename+"_q"+str(m)+".sgf", game, board, args.sgf_file)
        query.analyseTurn(m)
        engine.submitQuery(query)

        while not query.hasResult():
            engine.pollResult()
        
        #query.printResult()
        if args.anki:
            query.outputToAnki(args.outDir)
        else:
            query.outputToSGF(args.outDir)