"""
Unit tests for the `sort` application in PKU Shell.

Covers sorting files and stdin, reverse sort, error handling
for invalid options, missing files, and multiple arguments.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestSortApp(unittest.TestCase):
    def setUp(self):
        """Create and enter a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up and return to the original working directory."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin=None) -> str:
        """Run shell command with optional stdin and return output."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_sort_basic_eval(self):
        """Test basic sort from file input."""
        file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(file_path, "w") as f:
            f.write("banana\napple\ncherry\n")
        result = self.run_eval(f"sort {file_path}")
        self.assertEqual(result, "apple\nbanana\ncherry")

    def test_sort_reverse_eval(self):
        """Test reverse sort from file input."""
        file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(file_path, "w") as f:
            f.write("banana\napple\ncherry\n")
        result = self.run_eval(f"sort -r {file_path}")
        self.assertEqual(result, "cherry\nbanana\napple")

    def test_sort_stdin_eval(self):
        """Test sorting via stdin input."""
        input_data = "zebra\nmonkey\napple\n"
        result = self.run_eval("sort", stdin=input_data)
        self.assertEqual(result, "apple\nmonkey\nzebra")

    def test_sort_stdin_reverse_eval(self):
        """Test reverse sorting via stdin input."""
        input_data = "zebra\nmonkey\napple\n"
        result = self.run_eval("sort -r", stdin=input_data)
        self.assertEqual(result, "zebra\nmonkey\napple")

    def test_sort_missing_file_eval(self):
        """Test sort with missing file input."""
        result = self.run_eval("sort nonexistent.txt")
        self.assertIn("No such file", result)

    def test_sort_invalid_option_eval(self):
        """Test sort with an invalid flag."""
        with open("file.txt", "w") as f:
            f.write("sample")
        result = self.run_eval("sort -x file.txt")
        self.assertIn("unknown option -x", result)

    def test_sort_too_many_args_eval(self):
        """Test sort with multiple file arguments (unsupported)."""
        with open("file1.txt", "w") as f:
            f.write("a\nb\n")
        with open("file2.txt", "w") as f:
            f.write("c\nd\n")
        result = self.run_eval("sort -r file1.txt file2.txt")
        self.assertIn("wrong number of command line arguments", result)


if __name__ == "__main__":
    unittest.main()
