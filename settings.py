import json
import os

def load_settings(path="settings.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл настроек '{path}' не найден.")

    with open(path, "r", encoding="utf-8") as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Файл настроек содержит некорректный JSON.")

    if "board_size" not in settings:
        raise KeyError("В настройках должен быть указан 'board_size'.")

    return settings
