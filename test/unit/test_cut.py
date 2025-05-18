"""
Unit tests for the `cut` application in PKU Shell.

Tests cover byte selection using -b flag, both from files and from stdin input.
"""

import unittest
from collections import deque
import os
import tempfile
from shell import eval


class TestCutApp(unittest.TestCase):
    def setUp(self):
        """Create a temp directory and a sample input file."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        self.sample_file = os.path.join(self.test_dir.name, "sample.txt")
        with open(self.sample_file, "w") as f:
            f.write("ABC\nDEF\nGHI\nJKL\nMNO\n")

    def tearDown(self):
        """Restore working directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, stdin: str = None) -> str:
        """Run a shell command with optional stdin."""
        out = deque()
        eval(cmdline, out, stdin=stdin)
        return "".join(out)

    def test_cut_b_via_shell(self):
        """Test cutting the first byte from each line in a file."""
        result = self.run_eval(f"cut -b 1 {self.sample_file}")
        self.assertEqual(result, "A\nD\nG\nJ\nM\n")

    def test_cut_b_multiple_via_shell(self):
        """Test cutting byte range 1-2 from each line in a file."""
        result = self.run_eval(f"cut -b 1-2 {self.sample_file}")
        self.assertEqual(result, "AB\nDE\nGH\nJK\nMN\n")

    def test_cut_b_stdin_via_shell(self):
        """Test cutting bytes from stdin input."""
        input_data = "hello\nworld\ncut\ntest\nstdin"
        result = self.run_eval("cut -b 1-3", stdin=input_data)
        self.assertEqual(result, "hel\nwor\ncut\ntes\nstd\n")


if __name__ == "__main__":
    unittest.main()
