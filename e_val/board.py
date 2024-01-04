
class Board:
    def __init__(self, size=19):
        self._size = size
        self._board = [['.'] * size for i in range(19)]
        self._move = 0


    def in_bounds(self, x, y):
        return not (x >= self._size or y >= self._size or x < 0 or y < 0)

    def is_empty(self, x, y):
        if self.in_bounds(x, y):
            return self._board[x][y] == '.'
        return False

    def is_color(self, x, y, color):
        if self.in_bounds(x, y):
            return self._board[x][y] == color
        return False

    def _get_group(self, x, y, color, visited):
        if (x, y) in visited:
            return visited
        to_visit = []
        for (newx, newy) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if self.is_color(newx, newy, color):
                to_visit.append((newx, newy))
        visited[(x, y)] = True
        for (newx, newy) in to_visit:
            self._get_group(newx, newy, color, visited)
        return visited
        

    def _find_empty_neighbor(self, x, y):
        if not self.in_bounds(x, y):
            return True
        group = self._get_group(x, y, self._board[x][y], {})
        for (x, y) in group:
            for (newx, newy) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if self.is_empty(newx, newy):
                    return True
        return False

        
    # no ko rule
    def _move_is_legal(self, x, y):
        if x >= self._size or y >= self._size or x < 0 or y < 0:
            return False

        # a move that captures a stone is always legal
        self._remove_captures(x, y)

        if self._find_empty_neighbor(x, y):
            return True
        return False

    def _remove_captures(self, x, y):
        color = self._board[x][y]
        other_color = 'b'
        if color == 'b':
            other_color = 'w'
        for (newx, newy) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if self.is_color(newx, newy, other_color):
                if not self._find_empty_neighbor(newx, newy):
                    for (thirdx, thirdy) in self._get_group(newx, newy, other_color, {}):
                        self._board[thirdx][thirdy] = '.'

    def add_move(self, color, x, y):
        if not self.in_bounds(x, y):
            return False

        previous = self._board[x][y]
        self._board[x][y] = color
        if self._move_is_legal(x, y):
            self._move += 1
            return True

        self._board[x][y] = previous
        return False

    def output_points(self):
        black_points = []
        white_points = []
        for i in range(self._size):
            for j in range(self._size):
                if self._board[i][j] == 'b':
                    black_points.append((i, j)) 
                elif self._board[i][j] == 'w':
                    white_points.append((i, j))
        return (black_points, white_points) 

        
