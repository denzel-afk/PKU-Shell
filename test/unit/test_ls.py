"""
Unit tests for the `ls` application in PKU Shell.

Covers directory listing, path-specific listing, and error handling
for invalid paths in both safe and unsafe variants.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestLsApp(unittest.TestCase):
    def setUp(self):
        """Set up a temporary working directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Restore original working directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, command: str) -> str:
        """Run shell command and return output string."""
        out = deque()
        eval(command, out)
        return "".join(out).strip()

    def test_ls_safe_valid(self):
        """Test ls output when listing current directory contents."""
        os.mkdir("dir1")
        os.mkdir("dir2")
        with open("file1.txt", "w"):
            pass
        with open(".hidden.txt", "w"):
            pass
        result = self.run_eval("ls")
        names = result.split()
        self.assertEqual(set(names), {"dir1", "dir2", "file1.txt"})

    def test_ls_safe_with_path(self):
        """Test ls with a specific directory path."""
        folder = os.path.join(self.test_dir.name, "myfolder")
        os.mkdir(folder)
        with open(os.path.join(folder, "file.txt"), "w") as f:
            f.write("hi")
        result = self.run_eval(f"ls {folder}")
        self.assertEqual(result, "file.txt")

    def test_ls_safe_invalid_path(self):
        """Test ls with a non-existent path (safe variant)."""
        result = self.run_eval("ls no/such/dir")
        self.assertIn("No such directory", result)

    def test_ls_unsafe_invalid_path(self):
        """Test _ls with a non-existent path (unsafe variant)."""
        result = self.run_eval("_ls no/such/dir")
        self.assertIn("No such directory", result)


if __name__ == "__main__":
    unittest.main()
