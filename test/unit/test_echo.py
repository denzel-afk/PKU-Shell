"""
Unit tests for the `echo` application in PKU Shell.

Covers basic echo usage, quoting behavior, and command substitution.
"""

import unittest
import os
import sys
from collections import deque

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../src")
    )
)
from shell import eval  # noqa: E402


class TestEchoApp(unittest.TestCase):
    def run_eval(self, cmdline: str, stdin: str = None) -> str:
        """Run a shell command and return the output string."""
        out = deque()
        eval(cmdline, out, stdin=stdin)
        return "".join(out)

    def test_echo_safe_shell(self):
        """Test basic echo with multiple arguments."""
        result = self.run_eval("echo foo bar")
        self.assertEqual(result, "foo bar\n")

    def test_echo_single_quoted(self):
        """Test echo with single-quoted argument (preserve spaces)."""
        result = self.run_eval("echo 'foo  bar'")
        self.assertEqual(result, "foo  bar\n")

    def test_echo_double_quoted(self):
        """Test echo with double-quoted argument (preserve spaces)."""
        result = self.run_eval('echo "foo  bar"')
        self.assertEqual(result, "foo  bar\n")

    def test_echo_unsafe_shell(self):
        """Test echo via command substitution (e.g., `echo echo`)."""
        result = self.run_eval("`echo echo` foo bar")
        self.assertEqual(result, "foo bar\n")


if __name__ == "__main__":
    unittest.main()
