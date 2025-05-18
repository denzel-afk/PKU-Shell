"""
Unit tests for the `cd` application in PKU Shell.

Tests include valid and invalid directory changes,
handling of missing arguments,
and behavior of the unsafe `_cd` variant.
"""

import unittest
import os
from collections import deque
import tempfile
from shell import eval


class TestCdApp(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and switch to it."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Return to original directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str, cwd=None):
        """Run the shell command and return the output."""
        if cwd:
            os.chdir(cwd)
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_cd_safe_valid(self):
        """Test changing to a valid directory."""
        testdir_path = os.path.join(self.test_dir.name, "testdir")
        os.mkdir(testdir_path)
        self.run_eval("cd testdir")
        self.assertTrue(os.getcwd().endswith("testdir"))

    def test_cd_safe_invalid(self):
        """Test cd with no arguments (invalid usage)."""
        result = self.run_eval("cd")
        self.assertIn("wrong number of command line arguments", result)

    def test_cd_safe_invalid_path(self):
        """Test cd to a non-existent directory (safe)."""
        result = self.run_eval("cd nosuchdir")
        self.assertIn("No such directory", result)

    def test_cd_unsafe_invalid(self):
        """Test _cd to a non-existent directory (unsafe)."""
        result = self.run_eval("_cd nosuchdir")
        self.assertIn("No such directory", result)


if __name__ == "__main__":
    unittest.main()
