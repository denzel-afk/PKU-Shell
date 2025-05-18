"""
Unit tests for the `head` application in PKU Shell.

Tests include default line output, custom -n line count,
stdin support, and error handling for missing files.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestHeadApp(unittest.TestCase):
    def setUp(self):
        """Create temporary test directory and change into it."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Restore working directory and remove temp files."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin=None) -> str:
        """Run the shell command with optional stdin and return output."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_head_shell_default(self):
        """Test head default: first 10 lines of file."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(str(i) for i in range(1, 21)))
        result = self.run_eval(f"head {file_path}")
        expected = "\n".join(str(i) for i in range(1, 11))
        self.assertEqual(result, expected)

    def test_head_shell_n_argument(self):
        """Test head -n option to limit output lines."""
        file_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(file_path, "w") as f:
            f.write("\n".join(str(i) for i in range(1, 21)))
        result = self.run_eval(f"head -n 5 {file_path}")
        expected = "\n".join(str(i) for i in range(1, 6))
        self.assertEqual(result, expected)

    def test_head_shell_stdin(self):
        """Test head reading from stdin."""
        data = "\n".join(["one", "two", "three", "four", "five"])
        result = self.run_eval("head", stdin=data)
        self.assertEqual(result, data)

    def test_head_shell_file_not_found(self):
        """Test head with a missing file."""
        result = self.run_eval("head no_such_file.txt")
        self.assertIn("No such file", result)


if __name__ == "__main__":
    unittest.main()
