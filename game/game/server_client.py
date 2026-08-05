class ServerClient:
    def get_move(self, color):
        raise NotImplementedError

    def send_move(self, color, move):
        raise NotImplementedError


class FakeServerClient(ServerClient):
    def __init__(self):
        self.moves = {
            "B": [(2, 3), (3, 4)],
            "W": [(4, 5), (5, 6)]
        }
        self.call_count = {"B": 0, "W": 0}

    def get_move(self, color):
        moves = self.moves.get(color, [])
        i = self.call_count[color]
        self.call_count[color] += 1
        if i < len(moves):
            return moves[i]
        return None  # Эмуляция: больше ходов нет

    def send_move(self, color, move):
        print(f"Fake-сервер принял ход {color}: {move}")
