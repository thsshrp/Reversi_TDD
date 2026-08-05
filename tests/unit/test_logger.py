import unittest
import os
from game.logger_config import get_logger

class TestLoggerToFile(unittest.TestCase):
    def test_log_file_written(self):
        logfile = "test_game.log"
        if os.path.exists(logfile):
            os.remove(logfile)

        logger = get_logger(logfile)
        logger.info("Проверка записи лога")

        self.assertTrue(os.path.exists(logfile), "Файл логов должен быть создан")

        with open(logfile, "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertIn("Проверка записи лога", contents)

    def test_logger_is_singleton_like(self):
        logfile = "test_game.log"

        logger1 = get_logger(logfile)
        logger2 = get_logger(logfile)

        logger1.info("Одно сообщение")

        with open(logfile, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert sum("Одно сообщение" in line for line in lines) == 1, "Сообщение должно быть записано один раз"
