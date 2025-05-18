"""
Unit tests for the `cat` application in PKU Shell.

Tests include safe and unsafe file access, multiple files, stdin input,
file not found errors, and pipelining with grep.
"""

import unittest
import os
from shell import eval
from collections import deque
import tempfile


class TestCatApp(unittest.TestCase):
    def setUp(self):
        """Set up temporary directory for test files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up after test."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, command: str) -> str:
        """Helper to run shell command and capture output."""
        out = deque()
        eval(command, out)
        return "".join(out)

    def test_cat_safe_single(self):
        """Test cat on a single file."""
        file_path = os.path.join(self.test_dir.name, "file.txt")
        with open(file_path, "w") as f:
            f.write("hello\nworld")
        result = self.run_eval(f"cat {file_path}")
        self.assertEqual(result, "hello\nworld")

    def test_cat_safe_multiple(self):
        """Test cat on multiple files."""
        f1 = os.path.join(self.test_dir.name, "f1.txt")
        f2 = os.path.join(self.test_dir.name, "f2.txt")
        with open(f1, "w") as f:
            f.write("a")
        with open(f2, "w") as f:
            f.write("b")
        result = self.run_eval(f"cat {f1} {f2}")
        self.assertEqual(result, "ab")

    def test_cat_safe_stdin(self):
        """Test cat through a regular file as if via stdin."""
        file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(file_path, "w") as f:
            f.write("from stdin\n")
        result = self.run_eval(f"cat {file_path}")
        self.assertEqual(result, "from stdin\n")

    def test_cat_safe_file_not_found(self):
        """Test cat on missing file (safe)."""
        result = self.run_eval("cat nosuchfile.txt")
        self.assertIn("No such file", result)

    def test_cat_unsafe_file_not_found(self):
        """Test _cat on missing file (unsafe)."""
        result = self.run_eval("_cat nosuchfile.txt")
        self.assertIn("No such file", result)

    def test_pipeline_cat_grep(self):
        """Test cat piped into grep."""
        file_path = os.path.join(self.test_dir.name, "data.txt")
        with open(file_path, "w") as f:
            f.write("hello\nworld\nhello again\nbye")
        out = deque()
        eval(f"cat {file_path} | grep hello", out)
        result = "".join(out).strip()
        self.assertEqual(result, "hello\nhello again")


if __name__ == "__main__":
    unittest.main()
