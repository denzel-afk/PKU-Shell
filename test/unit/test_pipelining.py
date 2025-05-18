"""
Unit test for piped command execution in PKU Shell.

This test checks the correctness of multi-stage pipelines combining
cat, sort, and uniq commands to eliminate duplicates after sorting.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestPipelineApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temp directory and input files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        os.makedirs("dir1", exist_ok=True)
        with open("dir1/file1.txt", "w") as f:
            f.write("AAA\nBBB\nAAA\nCCC\n")
        with open("dir1/file2.txt", "w") as f:
            f.write("AAA\n")

    def tearDown(self):
        """Restore working directory and clean up temp files."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_shell(self, cmdline):
        """Run a shell command and return output as string."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_pipe_chain_sort_uniq_with_CCC(self):
        """Test chained pipeline: cat | sort | uniq."""
        result = self.run_shell(
            "cat dir1/file1.txt dir1/file2.txt | sort | uniq"
        )
        self.assertEqual(result.splitlines(), ["AAA", "BBB", "CCC"])


if __name__ == "__main__":
    unittest.main()
