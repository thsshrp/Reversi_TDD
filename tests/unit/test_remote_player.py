import unittest
from unittest.mock import Mock

from game.game.server_client import FakeServerClient
from game.remote_player import RemotePlayer

class TestRemotePlayer(unittest.TestCase):
    def test_remote_player_calls_get_move(self):
        client = Mock()
        client.get_move.return_value = (2, 3)

        player = RemotePlayer("B", client)

        move = player.make_move()

        client.get_move.assert_called_once_with("B")
        self.assertEqual(move, (2, 3))
class TestFakeServerClient(unittest.TestCase):
    def test_fake_server_returns_moves_in_sequence(self):
        client = FakeServerClient()

        move1 = client.get_move("B")
        move2 = client.get_move("B")
        move3 = client.get_move("B")

        self.assertEqual(move1, (2, 3))
        self.assertEqual(move2, (3, 4))
        self.assertIsNone(move3)

class TestRemotePlayerWithFakeServer(unittest.TestCase):
    def test_remote_player_uses_fake_server(self):
        client = FakeServerClient()
        player = RemotePlayer("B", client)

        move1 = player.make_move()
        move2 = player.make_move()
        move3 = player.make_move()

        self.assertEqual(move1, (2, 3))
        self.assertEqual(move2, (3, 4))
        self.assertIsNone(move3)