"""
Unit tests for the `wc` application in PKU Shell.

Covers line, word, and character counting from file and stdin,
with and without flags.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestWcApp(unittest.TestCase):
    def setUp(self):
        """Create and enter a temporary test directory with sample file."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        self.file_path = os.path.join(self.test_dir.name, "file1.txt")
        with open(self.file_path, "w") as f:
            f.write("AAA\nBBB\nAAA\n")

    def tearDown(self):
        """Restore working directory and clean up temp files."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin=None) -> str:
        """Run a shell command and return output string."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_wc_all_counts_eval(self):
        """Test wc with default mode (lines, words, characters)."""
        result = self.run_eval(f"wc {self.file_path}")
        self.assertEqual(result, "3 3 12")

    def test_wc_lines_eval(self):
        """Test wc with -l (line count) flag."""
        result = self.run_eval(f"wc -l {self.file_path}")
        self.assertEqual(result, "3")

    def test_wc_words_eval(self):
        """Test wc with -w (word count) flag."""
        result = self.run_eval(f"wc -w {self.file_path}")
        self.assertEqual(result, "3")

    def test_wc_chars_eval(self):
        """Test wc with -m (character count) flag."""
        result = self.run_eval(f"wc -m {self.file_path}")
        self.assertEqual(result, "12")

    def test_wc_stdin_eval(self):
        """Test wc reading from stdin (no flags)."""
        data = "AAA\nBBB\nAAA\n"
        result = self.run_eval("wc", stdin=data)
        self.assertEqual(result, "3 3 12")

    def test_wc_stdin_lines_eval(self):
        """Test wc -l with stdin input."""
        data = "AAA\nBBB\nAAA\n"
        result = self.run_eval("wc -l", stdin=data)
        self.assertEqual(result, "3")

    def test_wc_stdin_words_eval(self):
        """Test wc -w with stdin input."""
        data = "AAA\nBBB\nAAA\n"
        result = self.run_eval("wc -w", stdin=data)
        self.assertEqual(result, "3")

    def test_wc_stdin_chars_eval(self):
        """Test wc -m with stdin input."""
        data = "AAA\nBBB\nAAA\n"
        result = self.run_eval("wc -m", stdin=data)
        self.assertEqual(result, "12")


if __name__ == "__main__":
    unittest.main()
