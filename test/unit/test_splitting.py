"""
Unit tests for argument splitting in PKU Shell.

Covers word concatenation, single and double quotes, and quoted shell keywords.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestSplittingAndQuoting(unittest.TestCase):
    def setUp(self):
        """Create and enter a temporary directory for test isolation."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Restore working directory and clean up temp resources."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_shell(self, cmdline):
        """Run a shell command and return the stripped output."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_simple_splitting(self):
        """Test word concatenation without spaces using mixed quoting."""
        result = self.run_shell('echo a"b"c')
        self.assertEqual(result, "abc")

    def test_singlequotes(self):
        """Test single-quoted string preserves whitespace."""
        result = self.run_shell("echo 'a  b'")
        self.assertEqual(result, "a  b")

    def test_doublequotes(self):
        """Test double-quoted string preserves whitespace."""
        result = self.run_shell('echo "a  b"')
        self.assertEqual(result, "a  b")

    def test_disabled_doublequotes(self):
        """Test echoing double quotes inside single quotes."""
        result = self.run_shell("echo '\"\"'")
        self.assertEqual(result, "\"\"")

    def test_quote_keyword(self):
        """Test quoting a shell keyword character."""
        result = self.run_shell("echo ';'")
        self.assertEqual(result, ";")


if __name__ == "__main__":
    unittest.main()
