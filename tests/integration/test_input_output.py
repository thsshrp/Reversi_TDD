import unittest
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from game.board import Board
from game.constants import BLACK


class TestBoardDisplay(unittest.TestCase):
    def test_display_prints_correctly(self):
        board = Board()
        output = StringIO()
        with redirect_stdout(output):
            board.display()
        result = output.getvalue()
        self.assertIn("1 2 3 4 5 6 7 8", result)
        self.assertIn("4", result)
        self.assertIn("5", result)


class TestHumanInput(unittest.TestCase):
    def test_human_input_valid(self):
        from main import HumanPlayer
        player = HumanPlayer(BLACK)

        user_input = StringIO("3 4\n")
        output = StringIO()

        with redirect_stdout(output), redirect_stderr(output), unittest.mock.patch('sys.stdin', user_input):
            x, y = player.make_move()

        self.assertEqual((x, y), (3, 4))
