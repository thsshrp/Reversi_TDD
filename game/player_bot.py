import random

class RandomBot:
    def __init__(self, color, board, logger=None):
        self.color = color
        self.board = board
        self.logger = logger

    def __str__(self):
        return f"Бот ({self.color})"

    def make_move(self):
        valid_moves = self.board.get_valid_moves(self.color)
        if not valid_moves:
            if self.logger:
                self.logger.info(f"{self} пропускает ход — нет доступных ходов.")
            return None
        return random.choice(valid_moves)
