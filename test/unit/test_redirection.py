"""
Unit tests for input and output redirection in PKU Shell.

Covers standard input redirection using different syntax styles,
and verifies correct behavior of output redirection to files.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestRedirectionApp(unittest.TestCase):
    def setUp(self):
        """Create temporary directory and sample input file for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        with open("test.txt", "w") as f:
            f.write("foo")

    def tearDown(self):
        """Restore original working directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_shell(self, cmdline):
        """Run shell command and return stripped output."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_input_redirection(self):
        """Test input redirection using 'cat < file'."""
        result = self.run_shell("cat < test.txt")
        self.assertEqual(result, "foo")

    def test_input_redirection_infront(self):
        """Test input redirection in front position: '< file cat'."""
        result = self.run_shell("< test.txt cat")
        self.assertEqual(result, "foo")

    def test_input_redirection_nospace(self):
        """Test input redirection with no space: 'cat <file'."""
        result = self.run_shell("cat <test.txt")
        self.assertEqual(result, "foo")

    def test_output_redirection(self):
        """Test output redirection: 'echo hello > output.txt'."""
        self.run_shell("echo hello > output.txt")
        with open("output.txt", "r") as f:
            result = f.read().strip()
        self.assertEqual(result, "hello")


if __name__ == "__main__":
    unittest.main()
