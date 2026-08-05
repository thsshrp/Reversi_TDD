from unittest.mock import MagicMock
import unittest
import copy
from game.board import Board
from game.constants import BLACK, WHITE, EMPTY

class TestBoardPythonCoords(unittest.TestCase):
    def setUp(self):
        self.board = Board(human_coords=False)

    def test_initial_white_position(self):
        self.assertEqual(self.board.grid[3][3], WHITE)
        self.assertEqual(self.board.grid[4][4], WHITE)

    def test_initial_black_position(self):
        self.assertEqual(self.board.grid[3][4], BLACK)
        self.assertEqual(self.board.grid[4][3], BLACK)

    def test_out_of_bounds_move(self):
        for x, y in [(-1,0),(8,0),(0,-1),(0,8)]:
            self.assertFalse(self.board.is_valid_move(x,y,BLACK))
            self.assertFalse(self.board.is_valid_move(x,y,WHITE))

    def test_occupied_cell_move(self):
        self.board.grid[3][3] = BLACK
        self.assertFalse(self.board.is_valid_move(3,3,WHITE))
        self.board.grid[4][4] = WHITE
        self.assertFalse(self.board.is_valid_move(4,4,BLACK))

    def test_no_flips_move(self):
        self.assertFalse(self.board.is_valid_move(0,0,BLACK))
        self.assertFalse(self.board.is_valid_move(7,7,WHITE))
        self.assertFalse(self.board.is_valid_move(7,7,BLACK))
        self.assertFalse(self.board.is_valid_move(0,0,WHITE))

    def test_make_horizontal_flip(self):
        self.board.grid[3][2] = BLACK
        self.assertTrue(self.board.make_move(3,1,WHITE))
        self.assertEqual(self.board.grid[3][2], WHITE)

    def test_make_diagonal_flip(self):
        self.board.grid[2][2] = BLACK
        self.assertTrue(self.board.make_move(1,1,WHITE))
        self.assertEqual(self.board.grid[2][2], WHITE)

    def test_initial_score(self):
        self.assertEqual(self.board.get_score(), {'BLACK':2,'WHITE':2})

    def test_score_after_move(self):
        self.board.make_move(2,4,WHITE)
        self.assertEqual(self.board.get_score(), {'BLACK':1,'WHITE':4})



    def test_valid_moves_are_valid(self):
        moves = self.board.get_valid_moves(BLACK)
        for x, y in moves:
            self.assertTrue(
                self.board.is_valid_move(x, y, BLACK),
                msg=f"Move {(x, y)} returned but is_valid_move is False"
            )

    def test_valid_move_flips_pieces(self):
        for x, y in self.board.get_valid_moves(BLACK):
            b = copy.deepcopy(self.board)
            pre = b.get_score()
            made = b.make_move(x, y, BLACK)
            post = b.get_score()
            self.assertTrue(made, msg=f"make_move failed on valid move {(x, y)}")
            self.assertGreater(post['BLACK'], pre['BLACK'],
                               msg=f"No BLACK pieces flipped on move {(x, y)}")
            self.assertLess(post['WHITE'], pre['WHITE'],
                            msg=f"No WHITE pieces flipped on move {(x, y)}")

    def test_no_false_positives(self):
        valid = set(self.board.get_valid_moves(BLACK))
        for x in range(self.board.size):
            for y in range(self.board.size):
                if (x, y) not in valid:
                    self.assertFalse(
                        self.board.is_valid_move(x, y, BLACK),
                        msg=f"Move {(x, y)} is invalid but was not returned"
                    )
#
#
    def test_has_valid_move_true(self):
      self.assertTrue(self.board.has_valid_move(BLACK))
#
    def test_has_valid_move_false(self):
        self.board.grid = [[BLACK] * 8 for _ in range(8)]
        self.assertFalse(self.board.has_valid_move(WHITE))
#
    def test_game_over_and_winner(self):
        flat = [BLACK] * 30 + [WHITE] * 34
        self.board.grid = [flat[i * 8:(i + 1) * 8] for i in range(8)]

        self.assertFalse(self.board.has_valid_move(BLACK))
        self.assertFalse(self.board.has_valid_move(WHITE))

        score = self.board.get_score()
        self.assertEqual(score, {'BLACK': 30, 'WHITE': 34},
                         "get_score должен вернуть корректное число фишек")

        winner = 'WHITE' if score['WHITE'] > score['BLACK'] else 'BLACK'
        self.assertEqual(winner, 'WHITE',
                         "Победителем должен быть игрок с большим числом фишек")

    def test_make_vertical_flip_down(self):

        self.board.grid[2][3] = BLACK
        self.board.grid[3][3] = WHITE
        self.assertTrue(self.board.make_move(1, 3, WHITE))
        self.assertEqual(self.board.grid[2][3], WHITE)

    def test_make_vertical_flip_up(self):

        self.board.grid[3][3] = BLACK
        self.board.grid[4][3] = WHITE
        self.assertTrue(self.board.make_move(2, 3, WHITE))
        self.assertEqual(self.board.grid[3][3], WHITE)

    def test_get_valid_moves_initial(self):
        valid_moves = self.board.get_valid_moves(BLACK)
        expected = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertCountEqual(valid_moves, expected)

    def test_make_move_in_corner_flips(self):
        self.board.grid[0][0] = EMPTY
        self.board.grid[0][1] = WHITE
        self.board.grid[0][2] = BLACK

        self.assertTrue(self.board.make_move(0, 0, BLACK))
        self.assertEqual(self.board.grid[0][1], BLACK)


        self.board.grid = [[EMPTY] * 8 for _ in range(8)]
        self.board.grid[0][0] = EMPTY
        self.board.grid[1][0] = WHITE
        self.board.grid[2][0] = BLACK

        self.assertTrue(self.board.make_move(0, 0, BLACK))
        self.assertEqual(self.board.grid[1][0], BLACK)

    def test_make_move_in_corner_diagonal_flip(self):
        self.board.grid[0][0] = EMPTY
        self.board.grid[1][1] = WHITE
        self.board.grid[2][2] = BLACK

        self.assertTrue(self.board.make_move(0, 0, BLACK))
        self.assertEqual(self.board.grid[1][1], BLACK)

    def test_make_move_invalid_does_not_change_board(self):
        before = [row[:] for row in self.board.grid]
        result = self.board.make_move(0, 0, BLACK)
        after = self.board.grid
        self.assertFalse(result)
        self.assertEqual(before, after)

    def test_score_after_multiple_moves(self):

        self.board.make_move(5, 4, BLACK)
        self.board.make_move(3, 5, WHITE)
        score = self.board.get_score()

        total = score['BLACK'] + score['WHITE']
        self.assertEqual(total, 4 + 2)
        self.assertTrue(score['BLACK'] >= 2)
        self.assertTrue(score['WHITE'] >= 2)

    def test_get_valid_moves_no_moves(self):
        self.board.grid = [[BLACK] * 8 for _ in range(8)]
        moves = self.board.get_valid_moves(WHITE)
        self.assertEqual(moves, [])

    def test_game_over_and_winner_determination(self):
        self.board.grid = [
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, WHITE, WHITE, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, WHITE, WHITE, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
        ]

        self.assertFalse(self.board.has_valid_move(BLACK))
        self.assertFalse(self.board.has_valid_move(WHITE))

        score = self.board.get_score()
        self.assertEqual(score['BLACK'], 60)
        self.assertEqual(score['WHITE'], 4)

        winner = 'BLACK' if score['BLACK'] > score['WHITE'] else 'WHITE'
        self.assertEqual(winner, 'BLACK')
