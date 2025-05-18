"""
Unit tests for the `uniq` application in PKU Shell.

Covers case-sensitive and case-insensitive behavior, input from file and stdin,
handling of missing files, invalid flags, and excessive arguments.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestUniqApp(unittest.TestCase):
    def setUp(self):
        """Create and enter a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Restore working directory and clean up temp directory."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin=None) -> str:
        """Run shell command with optional stdin and return the output."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_uniq_file_eval(self):
        """Test uniq with case-sensitive input from file."""
        file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(file_path, "w") as f:
            f.write("AAA\naaa\nAAA\n")
        result = self.run_eval(f"uniq {file_path}")
        self.assertEqual(result, "AAA\naaa\nAAA")

    def test_uniq_stdin_eval(self):
        """Test uniq with case-sensitive input from stdin."""
        result = self.run_eval("uniq", stdin="AAA\naaa\nAAA\n")
        self.assertEqual(result, "AAA\naaa\nAAA")

    def test_uniq_i_file_eval(self):
        """Test uniq -i (ignore case) with file input."""
        file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(file_path, "w") as f:
            f.write("AAA\naaa\nAAA\n")
        result = self.run_eval(f"uniq -i {file_path}")
        self.assertEqual(result, "AAA")

    def test_uniq_i_stdin_eval(self):
        """Test uniq -i (ignore case) with stdin input."""
        result = self.run_eval("uniq -i", stdin="AAA\naaa\nAAA\n")
        self.assertEqual(result, "AAA")

    def test_uniq_missing_file_eval(self):
        """Test uniq with a non-existent file."""
        result = self.run_eval("uniq missing.txt")
        self.assertIn("uniq: missing.txt: No such file", result)

    def test_uniq_too_many_args_eval(self):
        """Test uniq with too many file arguments."""
        with open("file1.txt", "w") as f:
            f.write("a\nb\n")
        with open("file2.txt", "w") as f:
            f.write("c\nd\n")
        result = self.run_eval("uniq -i file1.txt file2.txt")
        self.assertIn(
            "uniq: wrong number of command line arguments or flags",
            result
        )

    def test_uniq_invalid_flag_eval(self):
        """Test uniq with an unsupported flag."""
        with open("file.txt", "w") as f:
            f.write("anything")
        result = self.run_eval("uniq -x file.txt")
        self.assertIn("uniq: wrong flags", result)


if __name__ == "__main__":
    unittest.main()
