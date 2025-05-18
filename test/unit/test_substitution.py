"""
Unit tests for command substitution behavior in PKU Shell.

Covers basic substitution, nested usage, splitting, semicolon handling,
quoted substitution, and command-as-application behavior.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestSubstitutionApp(unittest.TestCase):
    def setUp(self):
        """Set up temporary test directory and sample files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        with open("test.txt", "w") as f:
            f.write("''")

        os.makedirs("dir2/subdir", exist_ok=True)
        with open("dir2/subdir/file.txt", "w") as f:
            f.write("AAA\naaa\nAAA")

    def tearDown(self):
        """Clean up test environment and restore working directory."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_shell(self, cmdline):
        """Execute a shell command and return the output."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_substitution(self):
        """Test simple command substitution."""
        self.assertEqual(self.run_shell("echo `echo foo`"), "foo")

    def test_substitution_insidearg(self):
        """Test substitution inside a larger argument."""
        self.assertEqual(self.run_shell("echo a`echo a`a"), "aaa")

    def test_substitution_splitting(self):
        """Test substitution with multiple words."""
        self.assertEqual(self.run_shell("echo `echo foo  bar`"), "foo bar")

    def test_substitution_semicolon(self):
        """Test substitution containing semicolon-separated commands."""
        result = (
            self.run_shell("echo `echo foo; echo bar`")
            .replace("\n", " ")
            .strip()
        )
        self.assertEqual(result, "foo bar")

    def test_substitution_keywords(self):
        """Test substitution using file content as argument."""
        self.assertEqual(self.run_shell("echo `cat test.txt`"), "''")

    def test_substitution_app(self):
        """Test substitution as application name."""
        self.assertEqual(self.run_shell("`echo echo` foo"), "foo")


if __name__ == "__main__":
    unittest.main()
