"""
Unit tests for globbing behavior in PKU Shell.

Covers wildcard expansion for *.txt files in current and subdirectories.
"""

import unittest
import os
from pathlib import PurePath
from collections import deque
import tempfile
from shell import eval


class TestGlobbingApp(unittest.TestCase):
    def setUp(self):
        """Create a temp test directory with matching
        and non-matching files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        with open("test.txt", "w") as f:
            f.write("test")
        with open("skip.md", "w") as f:
            f.write("not included")

        os.makedirs("dir1", exist_ok=True)
        for name in ["file1.txt", "file2.txt", "longfile.txt"]:
            with open(os.path.join("dir1", name), "w") as f:
                f.write(name)

    def tearDown(self):
        """Reset working directory and clean up test environment."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str) -> str:
        """Run shell command and return its output."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_globbing_current_dir(self):
        """Test wildcard *.txt in current directory."""
        result = set(
            PurePath(p).as_posix()
            for p in self.run_eval("echo *.txt").split()
        )
        self.assertEqual(result, {"test.txt"})

    def test_globbing_subdirectory(self):
        """Test wildcard dir1/*.txt in subdirectory."""
        result = set(
            PurePath(p).as_posix()
            for p in self.run_eval("echo dir1/*.txt").split()
        )
        self.assertEqual(result, {
            "dir1/file1.txt",
            "dir1/file2.txt",
            "dir1/longfile.txt"
        })


if __name__ == "__main__":
    unittest.main()
