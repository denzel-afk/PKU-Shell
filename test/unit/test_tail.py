"""
Unit tests for the `tail` application in PKU Shell.

Covers default output, -n flag usage, stdin input,
edge cases like large -n and -n 0,
invalid flags, and missing file handling.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestTailApp(unittest.TestCase):
    def setUp(self):
        """Create and switch to temporary directory for isolated testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up temporary directory and return to original
        working directory."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin=None) -> str:
        """Run the shell command and return output string."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_tail_default_eval(self):
        """Test tail default behavior (last 10 lines)."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(str(i) for i in range(1, 21)))
        result = self.run_eval(f"tail {file_path}")
        expected = "\n".join(str(i) for i in range(11, 21))
        self.assertEqual(result, expected)

    def test_tail_n_argument_eval(self):
        """Test tail -n N for specific line count from file."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(str(i) for i in range(1, 21)))
        result = self.run_eval(f"tail -n 5 {file_path}")
        expected = "\n".join(str(i) for i in range(16, 21))
        self.assertEqual(result, expected)

    def test_tail_large_n_eval(self):
        """Test tail -n with value greater than total lines."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(str(i) for i in range(1, 11)))
        result = self.run_eval(f"tail -n 50 {file_path}")
        expected = "\n".join(str(i) for i in range(1, 11))
        self.assertEqual(result, expected)

    def test_tail_stdin_eval(self):
        """Test tail with input from stdin."""
        input_data = "\n".join(["a", "b", "c", "d", "e"])
        result = self.run_eval("tail", stdin=input_data)
        expected = "\n".join(["a", "b", "c", "d", "e"])
        self.assertEqual(result, expected)

    def test_tail_n0_eval(self):
        """Test tail with -n 0 (expect empty output)."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(["1", "2", "3", "4"]))
        result = self.run_eval(f"tail -n 0 {file_path}")
        self.assertEqual(result, "")

    def test_tail_invalid_flag_eval(self):
        """Test tail with unsupported flag."""
        with open("file.txt", "w") as f:
            f.write("test")
        result = self.run_eval("tail --x file.txt")
        self.assertIn("tail: wrong flags", result)

    def test_tail_missing_file_eval(self):
        """Test tail with a non-existent file."""
        result = self.run_eval("tail no_such_file.txt")
        self.assertIn("No such file", result)


if __name__ == "__main__":
    unittest.main()
