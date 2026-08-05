from game.constants import EMPTY, BLACK, WHITE


class Board:
    def __init__(self, size=8, human_coords=True):
        self.board = None
        self.size = size
        self.human_coords = human_coords
        self.grid = [[EMPTY] * size for _ in range(size)]
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)]

    def is_valid_move(self, x, y, player):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False

        if self.grid[x][y] != EMPTY:
            return False

        opponent = WHITE if player == BLACK else BLACK
        valid = False

        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == opponent:
                nx += dx
                ny += dy
                while 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.grid[nx][ny] == player:
                        valid = True
                        break
                    elif self.grid[nx][ny] == EMPTY:
                        break
                    nx += dx
                    ny += dy
                if valid:
                    break

        return valid

    def _convert_coords(self, x, y):
        return (x - 1, y - 1) if self.human_coords else (x, y)

    def make_move(self, x, y, player):
        x, y = self._convert_coords(x, y)

        if not self.is_valid_move(x, y, player):
            return False

        self._place_piece(x, y, player)
        self._apply_flips(x, y, player)
        return True

    def _place_piece(self, x, y, color):
        self.grid[x][y] = color

    def _apply_flips(self, x, y, player):
        opponent = self._get_opponent(player)
        for dx, dy in self.DIRECTIONS:
            self._flip_in_direction(x, y, dx, dy, player, opponent)

    def _get_opponent(self, player):
        return WHITE if player == BLACK else BLACK



    def _flip_in_direction(self, x, y, dx, dy, player, opponent):
        x += dx
        y += dy
        to_flip = []

        while 0 <= x < self.size and 0 <= y < self.size:
            if self.grid[x][y] == opponent:
                to_flip.append((x, y))
            elif self.grid[x][y] == player:
                for fx, fy in to_flip:
                    self.grid[fx][fy] = player
                return
            else:
                return
            x += dx
            y += dy

    #def print_board(self):
    #    """Выводит доску в консоль с координатами (1-8)"""
    #    print("  " + " ".join(str(i) for i in range(1, self.size + 1)))
    #    for i, row in enumerate(self.grid, 1):
    #        print(i, " ".join(row))
#
    def get_score(self):
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return {'BLACK': black, 'WHITE': white}

    def get_valid_moves(self, player):
        moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        if self.human_coords:
            return [(x + 1, y + 1) for (x, y) in moves]
        return moves

    def has_valid_move(self, player):
        for x in range(self.size):
            for y in range(self.size):
                if self.is_valid_move(x, y, player):
                    return True
        return False


    def display(self):
        symbols = {EMPTY: ".", BLACK: "B", WHITE: "W"}
        print("  " + " ".join(str(i + 1) for i in range(self.size)))
        for i, row in enumerate(self.grid):
            printable_row = [symbols.get(cell, "?") for cell in row]
            print(str(i + 1), " ".join(printable_row))

    def place_piece(self, x, y, color):
        self._place_piece(x, y, color)