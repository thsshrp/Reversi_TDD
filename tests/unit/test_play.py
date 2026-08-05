import unittest
from unittest.mock import Mock
from game.play import Play


class TestPlayOneTurn(unittest.TestCase):
    def setUp(self):
        self.board = Mock()
        self.board.get_valid_moves.return_value = [(3, 2)]
        self.board.place_piece = Mock()
        self.board.display = Mock()
        self.board.get_score.return_value = {"WHITE": 2, "BLACK": 3}

        self.player1 = Mock()
        self.player1.make_move.return_value = (3, 2)
        del self.player1.is_human

        self.player2 = Mock()
        del self.player2.is_human

        self.logger = Mock()
        self.game = Play(self.board, self.player1, self.player2, self.logger)

    def test_one_turn_should_update_board_and_switch_player_and_log(self):
        self.player1.make_move.return_value = (3, 2)
        self.player1.color = "B"
        self.board.place_piece = Mock()
        self.board.display = Mock()

        if hasattr(self.player1, "is_human"):
            del self.player1.is_human
        if hasattr(self.player2, "is_human"):
            del self.player2.is_human

        self.game.play_one_turn()

        self.board.place_piece.assert_called_with(3, 2, "B")
        self.assertEqual(self.game.current_player, self.player2)

    def test_play_game_ends_when_no_moves(self):
        board = Mock()
        board.get_valid_moves.return_value = []
        board.get_score.return_value = {"WHITE": 2, "BLACK": 3}
        board.display = Mock()
        board.place_piece = Mock()

        player1 = Mock()
        player2 = Mock()
        del player1.is_human
        del player2.is_human

        logger = Mock()
        game = Play(board, player1, player2, logger)

        game.play()
        logger.info.assert_called_with("Игра окончена: ни один игрок не может сделать ход.")

    def test_play_game_should_end_when_no_players_can_move(self):
        board = Mock()
        board.get_valid_moves.return_value = []
        board.get_score.return_value = {"WHITE": 2, "BLACK": 3}
        board.display = Mock()
        board.place_piece = Mock()

        player1 = Mock()
        player2 = Mock()
        del player1.is_human
        del player2.is_human

        logger = Mock()
        game = Play(board, player1, player2, logger)

        game.play()
        logger.info.assert_called_with("Игра окончена: ни один игрок не может сделать ход.")

    def test_play_one_turn_should_accept_valid_player_move(self):
        board = Mock()
        board.get_valid_moves.return_value = [(3, 4)]
        board.place_piece = Mock()
        board.display = Mock()

        player1 = Mock()
        player1.make_move.return_value = (3, 4)
        player1.color = "B"
        del player1.is_human

        player2 = Mock()
        del player2.is_human

        logger = Mock()
        game = Play(board, player1, player2, logger)

        game.play_one_turn()
        board.place_piece.assert_called_once_with(3, 4, "B")

    def test_play_should_skip_turn_if_current_player_has_no_moves(self):
        board = Mock()
        board.display = Mock()
        board.get_score.return_value = {"WHITE": 2, "BLACK": 3}
        board.place_piece = Mock()

        logger = Mock()
        player1 = Mock()
        player2 = Mock()
        del player1.is_human
        del player2.is_human

        play = Play(board, player1, player2, logger)
        play.play_one_turn = Mock()

        call_counter = {"count": 0}

        def fake_get_valid_moves(player):
            call_counter["count"] += 1
            if call_counter["count"] == 1:
                return []
            elif call_counter["count"] == 2:
                return [(2, 3)]
            elif call_counter["count"] in (3, 4):
                return []
            return []

        board.get_valid_moves.side_effect = fake_get_valid_moves
        play.play()

        logger.info.assert_called_with("Игра окончена: ни один игрок не может сделать ход.")

class TestPlayErrorHandling(unittest.TestCase):
    def test_play_one_turn_handles_connection_error(self):
        board = Mock()
        board.display = Mock()
        board.place_piece = Mock()
        board.get_valid_moves.return_value = [(3, 3)]
        logger = Mock()

        player1 = Mock()
        player1.make_move.return_value = (3, 3)
        player1.is_human = Mock(return_value=False)
        player1.color = "B"

        player2 = Mock()
        player2.make_move.side_effect = ConnectionError("Сервер недоступен")
        player2.is_human = Mock(return_value=False)
        player2.color = "W"

        game = Play(board, player1, player2, logger)

        game.play_one_turn()
        game.play_one_turn()
        assert game.current_player == player1

        logger.error.assert_called()
        args, _ = logger.error.call_args
        assert "Сервер недоступен" in args[0]