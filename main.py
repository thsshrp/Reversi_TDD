import argparse
import os
from game.board import Board
from game.play import Play
from game.logger_config import get_logger
from game.player_bot import RandomBot
from game.constants import BLACK, WHITE
from settings import load_settings


class HumanPlayer:
    def is_human(self):
        return True

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"Игрок ({self.color})"

    def make_move(self):
        while True:
            try:
                move = input(f"Ход игрока {self.color} (введите координаты (строка)X Y(столбец) через пробел): ")
                x, y = map(int, move.strip().split())
                return x, y
            except ValueError:
                print("Ошибка ввода. Введите два числа через пробел.")
class MockNetworkPlayer:
    def __init__(self, color):
        self.color = color

    def is_human(self):
        return False

    def __str__(self):
        return f"Сетевой игрок ({self.color})"

    def make_move(self):
        raise ConnectionError("Сетевой игрок недоступен. Сервер не отвечает.")


def select_players(mode, board, logger):
    if mode == "local":
        return HumanPlayer(BLACK), HumanPlayer(WHITE)
    elif mode == "bot":
        return HumanPlayer(BLACK), RandomBot(WHITE, board, logger)
    elif mode == "remote":
        return HumanPlayer(BLACK), MockNetworkPlayer(WHITE)
    else:
        print("Неверный режим. Запускаем Игрок vs Бот по умолчанию.")
        return HumanPlayer(BLACK), RandomBot(WHITE, board, logger)


def parse_args():
    parser = argparse.ArgumentParser(description="Консольная игра Реверси")

    parser.add_argument("--mode", choices=["local", "bot", "remote"],
                        help="Режим игры: local, bot, remote")
    parser.add_argument("--settings", default="settings.json",
                        help="Путь к JSON-файлу с настройками")
    parser.add_argument("--size", type=int,
                        help="Размер поля (переопределяет настройки)")
    parser.add_argument("--logfile", default="game.log",
                        help="Имя лог-файла")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        settings = load_settings(args.settings)
        size = args.size or settings.get("board_size")
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        size = args.size

    if not size:
        while True:
            try:
                size = int(input("Введите размер поля (например, 8): "))
                if size >= 4 and size % 2 == 0:
                    break
                else:
                    print("Размер должен быть чётным и ≥ 4.")
            except ValueError:
                print("Введите число.")

    board = Board(size=size)
    logger = get_logger(logfile=args.logfile)

    mode = args.mode
    if not mode:
        # Если не передан режим — спрашиваем вручную
        print("Выберите режим игры:")
        print("1 — Игрок vs Игрок")
        print("2 — Игрок vs Бот")
        print("3 — Игрок vs Удалённый игрок (через сервер-заглушку)")
        choice = input("Ваш выбор: ")
        mode = {"1": "local", "2": "bot", "3": "remote"}.get(choice, "bot")

    player1, player2 = select_players(mode, board, logger)
    print(f"\nИгра началась!")
    print(f"Игрок 1: {player1} — {'Чёрные (BLACK)' if player1.color == 1 else 'Белые (WHITE)'}")
    print(f"Игрок 2: {player2} — {'Чёрные (BLACK)' if player2.color == 1 else 'Белые (WHITE)'}")
    print(f"Первым ходит: {player1}\n")

    game = Play(board, player1, player2, logger)
    game.play()
