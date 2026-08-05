class RemotePlayer:
    def __init__(self, color, server_client):
        self.color = color
        self.client = server_client

    def __str__(self):
        return f"Удалённый игрок ({self.color})"

    def make_move(self):
        return self.client.get_move(self.color)
