"""
PKU Shell - Unit Test Entry Point

This script discovers and runs all unit tests located in the `test/unit/`
directory using Python's built-in unittest framework.

It is intended to be used inside a Docker container or locally to verify the
correctness and stability of the shell implementation.

Usage:
    python3 test_shell.py

In Docker:
    docker run -p 80:8000 -ti --rm shell /pku_shell/test_shell.py
"""

import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()

    suite = loader.discover('test/unit')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
