import unittest
import os
import json
from settings import load_settings

class TestSettings(unittest.TestCase):

    def setUp(self):
        self.valid_path = "test_valid_settings.json"
        self.invalid_json_path = "test_invalid_json.json"
        self.missing_key_path = "test_missing_key.json"
        self.nonexistent_path = "nonexistent_settings.json"

        # 1. валидный файл
        with open(self.valid_path, "w", encoding="utf-8") as f:
            json.dump({"board_size": 8}, f)

        # 2. битый JSON
        with open(self.invalid_json_path, "w", encoding="utf-8") as f:
            f.write("{ board_size: 8")

        # 3. нет ключа
        with open(self.missing_key_path, "w", encoding="utf-8") as f:
            json.dump({"some_other_key": 10}, f)

    def tearDown(self):
        for path in [
            self.valid_path,
            self.invalid_json_path,
            self.missing_key_path,
        ]:
            if os.path.exists(path):
                os.remove(path)

    def test_load_valid_settings(self):
        settings = load_settings(self.valid_path)
        self.assertEqual(settings["board_size"], 8)

    def test_missing_file_raises_exception(self):
        with self.assertRaises(FileNotFoundError):
            load_settings(self.nonexistent_path)

    def test_invalid_json_format_raises_exception(self):
        with self.assertRaises(ValueError):
            load_settings(self.invalid_json_path)

    def test_missing_required_key_raises_exception(self):
        with self.assertRaises(KeyError):
            load_settings(self.missing_key_path)
