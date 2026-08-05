import unittest
from unittest.mock import Mock
from game.player_bot import RandomBot
from game.constants import BLACK

class TestRandomBot(unittest.TestCase):
    def test_bot_chooses_valid_move(self):
        board = Mock()
        board.get_valid_moves.return_value = [(2, 3), (3, 4), (5, 6)]
        bot = RandomBot(BLACK, board)
        move = bot.make_move()
        self.assertIn(move, [(2, 3), (3, 4), (5, 6)], "Бот должен выбирать один из валидных ходов")

    def test_bot_returns_none_if_no_moves(self):
        board = Mock()
        board.get_valid_moves.return_value = []

        logger = Mock()
        bot = RandomBot("BLACK", board, logger=logger)

        move = bot.make_move()
        self.assertIsNone(move)
        logger.info.assert_called_with("Бот (BLACK) пропускает ход — нет доступных ходов.")

