import subprocess
import sys
import os
import unittest

class TestSystemRun(unittest.TestCase):
    def test_main_starts_and_exits_cleanly(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--mode", "remote", "--size", "4"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.abspath(os.path.dirname(__file__) + "/../../")
        )

        if result.returncode != 0:
            print("\n=== STDOUT ===")
            print(result.stdout.decode("utf-8", errors="ignore"))
            print("\n=== STDERR ===")
            print(result.stderr.decode("utf-8", errors="ignore"))

        self.assertEqual(result.returncode, 0)
