from unittest.mock import Mock

from game.constants import WHITE, BLACK


class Play:
    def __init__(self, board, player1, player2, logger):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.logger = logger
        self.current_player = player1

    def play_one_turn(self):
        try:
            move = self.current_player.make_move()
        except Exception as e:
            self.logger.error(f"Ошибка во время хода {self.current_player}: {e}")
            print(f"[СЕТЕВАЯ ОШИБКА] Ход игрока {self.current_player} невозможен: {e}")

            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            return

        if move is None:
            self.logger.info(f"{self.current_player} пропускает ход — нет доступных ходов.")
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            return

        row, col = move

        if hasattr(self.current_player, "is_human") and self.current_player.is_human():
            if not self.board.make_move(row, col, self.current_player.color):
                self.logger.info(f"{self.current_player} попытался сделать недопустимый ход: ({row}, {col})")
                print("Недопустимый ход. Попробуйте снова.")
                return
        else:
            self.board.place_piece(row, col, self.current_player.color)

        self.logger.info(f"{self.current_player} ходит на ({row + 1}, {col + 1})")
        self.board.display()
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play(self):
        self.board.display()
        skipped_turns = 0

        while True:
            player_color = self.current_player.color
            if player_color == 1:
                player_color = BLACK
            elif player_color == 2:
                player_color = WHITE

            valid_moves = self.board.get_valid_moves(player_color)
            print(f" Ходы для {self.current_player}: {valid_moves}")

            if not valid_moves:
                self.logger.info(f"{self.current_player} не может сделать ход.")
                print(f"{self.current_player} пропускает ход.")
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                skipped_turns += 1

                if skipped_turns >= 2:
                    self.logger.info("Игра окончена: ни один игрок не может сделать ход.")
                    score = self.board.get_score()
                    winner = "WHITE" if score["WHITE"] > score["BLACK"] else "BLACK"
                    print(f"Победил: {winner}! Счёт: {score}")
                    break
                continue

            skipped_turns = 0
            self.play_one_turn()


