"""
Unit tests for command sequencing with semicolons in PKU Shell.

Tests include sequential execution of multiple commands and behavior
when an earlier command in the sequence fails.
"""

import unittest
import os
import tempfile
from collections import deque
from shell import eval


class TestSequencingApp(unittest.TestCase):
    def setUp(self):
        """Set up temporary directory and dummy file."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

        with open("test.txt", "w") as f:
            f.write("")

    def tearDown(self):
        """Restore original directory and clean up."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def run_shell(self, cmdline):
        """Run shell command and return output as string."""
        out = deque()
        eval(cmdline, out)
        return "".join(out).strip()

    def test_semicolon(self):
        """Test two sequential commands separated by semicolon."""
        result = set(self.run_shell("echo AAA; echo BBB").split())
        self.assertEqual(result, {"AAA", "BBB"})

    def test_semicolon_chain(self):
        """Test three sequential commands chained with semicolons."""
        result = set(self.run_shell("echo AAA; echo BBB; echo CCC").split())
        self.assertEqual(result, {"AAA", "BBB", "CCC"})

    def test_semicolon_exception(self):
        """Test behavior when first command fails but second executes."""
        result = self.run_shell("ls dir3; echo BBB")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
