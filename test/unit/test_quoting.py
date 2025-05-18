"""
Unit tests for quoting in PKU Shell.

Covers single quotes, double quotes, nested quotes, and command substitution
within quoted strings.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestQuotingApp(unittest.TestCase):
    def setUp(self):
        """Create and enter temporary test directory."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Return to original directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str) -> str:
        """Run shell command and return its output."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_single_quotes(self):
        """Test echo with single quotes preserves whitespace."""
        result = self.run_eval("echo 'a  b'")
        self.assertEqual(result, "a  b")

    def test_quote_keyword(self):
        """Test echo with quoted shell keyword (;)."""
        result = self.run_eval("echo ';'")
        self.assertEqual(result, ";")

    def test_double_quotes(self):
        """Test echo with double quotes preserves whitespace."""
        result = self.run_eval('echo "a  b"')
        self.assertEqual(result, "a  b")

    def test_substitution_double_quotes(self):
        """Test command substitution inside double quotes."""
        result = self.run_eval('echo "`echo foo`"')
        self.assertEqual(result, "foo")

    def test_nested_double_quotes(self):
        """Test nested command substitution inside double quotes."""
        result = self.run_eval('echo "a `echo \\"b\\"`"')
        self.assertEqual(result, "a b")

    def test_disabled_double_quotes(self):
        """Test double quotes inside single quotes are not interpreted."""
        result = self.run_eval("echo '\"\"'")
        self.assertEqual(result, '""')


if __name__ == "__main__":
    unittest.main()
