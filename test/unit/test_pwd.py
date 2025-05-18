"""
Unit tests for the `pwd` application in PKU Shell.

Covers correct output of current directory and error handling
when too many arguments are provided.
"""

import unittest
import os
from collections import deque
from shell import eval as shell_eval


class TestPwdApp(unittest.TestCase):
    def run_eval(self, cmdline: str) -> str:
        """Run shell command and return output string."""
        out = deque()
        shell_eval(cmdline, out)
        return "".join(out).strip()

    def test_pwd_shell_valid(self):
        """Test pwd returns the current working directory."""
        result = self.run_eval("pwd")
        self.assertEqual(result, os.getcwd())

    def test_pwd_shell_invalid(self):
        """Test pwd with extra arguments returns error."""
        result = self.run_eval("pwd foo")
        self.assertIn("too many arguments", result)


if __name__ == "__main__":
    unittest.main()
