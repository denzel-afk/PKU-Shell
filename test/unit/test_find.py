"""
Unit tests for the `find` application in PKU Shell.

Tests include pattern matching using -name, finding all .txt files,
and scoped directory search.
"""

import unittest
import os
from collections import deque
import tempfile
from shell import eval


class TestFindApp(unittest.TestCase):
    def setUp(self):
        """Create test directory structure and test files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        with open("test.txt", "w") as f:
            f.write("''")

        os.makedirs("dir1", exist_ok=True)
        with open("dir1/file1.txt", "w") as f:
            f.write("AAA\nBBB\nAAA\n")
        with open("dir1/file2.txt", "w") as f:
            f.write("CCC\n")
        with open("dir1/longfile.txt", "w") as f:
            f.write("\n".join(str(i) for i in range(1, 21)))

        os.makedirs("dir2/subdir", exist_ok=True)
        with open("dir2/subdir/file.txt", "w") as f:
            f.write("AAA\naaa\nAAA\n")

    def tearDown(self):
        """Restore working directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_eval(self, cmdline: str) -> str:
        """Run a shell command and return output as string."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_find_exact_file(self):
        """Test finding a file with exact name match."""
        result = self.run_eval("find -name 'file.txt'")
        paths = set(result.splitlines())
        self.assertEqual(paths, {"./dir2/subdir/file.txt"})

    def test_find_all_txt(self):
        """Test finding all .txt files in nested directories."""
        result = self.run_eval("find -name '*.txt'")
        paths = set(result.splitlines())
        self.assertEqual(paths, {
            "./test.txt",
            "./dir1/file1.txt",
            "./dir1/file2.txt",
            "./dir1/longfile.txt",
            "./dir2/subdir/file.txt",
        })

    def test_find_from_dir(self):
        """Test finding .txt files starting from specific directory."""
        result = self.run_eval("find dir1 -name '*.txt'")
        paths = set(result.splitlines())
        self.assertEqual(paths, {
            "dir1/file1.txt",
            "dir1/file2.txt",
            "dir1/longfile.txt",
        })


if __name__ == "__main__":
    unittest.main()
