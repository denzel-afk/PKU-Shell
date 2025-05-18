"""
Unit tests for the `grep` application in PKU Shell.

Tests include pattern matching from files, stdin, and multiple file inputs.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval as shell_eval


class TestGrepApp(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up and restore original working directory."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline, stdin=None):
        """Execute shell command with optional stdin."""
        out = deque()
        shell_eval(cmdline, out, stdin=stdin)
        return "".join(out).strip()

    def test_grep_shell(self):
        """Test grep with a single file and pattern."""
        file_path = os.path.join(self.test_dir.name, "input.txt")
        with open(file_path, "w") as f:
            f.write("one\ntwo\nthree")
        result = self.run_eval(f"grep o {file_path}")
        self.assertEqual(result, "one\ntwo")

    def test_grep_shell_stdin(self):
        """Test grep reading from stdin input."""
        data = "AAA\nBBB\nCCC"
        result = self.run_eval("grep B", stdin=data)
        self.assertEqual(result, "BBB")

    def test_grep_multiple_files(self):
        """Test grep across multiple files, output includes filenames."""
        f1 = os.path.join(self.test_dir.name, "a.txt")
        f2 = os.path.join(self.test_dir.name, "b.txt")
        with open(f1, "w") as f:
            f.write("foo\nbar")
        with open(f2, "w") as f:
            f.write("baz\nfoo")
        result = self.run_eval(f"grep foo {f1} {f2}")
        expected = f"{f1}:foo\n{f2}:foo"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
