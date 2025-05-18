"""
Implementation of the `cd` shell application for PKU Shell.

Handles directory navigation by validating path existence and permissions.
Supports error reporting for invalid or inaccessible paths.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry
import os


class CdApp(BaseApp):
    """
    Application that implements the Unix-like `cd` command.

    Validates the target directory before changing into it.
    Returns an action dictionary instead of string output to
    trigger directory change in context.
    """

    def run(self, args, stdin=None):
        """
        Execute the cd command.

        Args:
            args (List[str]): List containing exactly one directory path.
            stdin (str, optional): Ignored for cd.

        Returns:
            dict: {"action": "chdir", "target": path} if successful.

        Raises:
            ValueError: If arguments are missing or directory is invalid.
        """
        if len(args) != 1:
            raise ValueError("cd: wrong number of command line arguments")

        path = args[0]
        self.validate_directory(path)
        return {"action": "chdir", "target": path}

    def validate_directory(self, path):
        """
        Check if a path is a valid and accessible directory.

        Args:
            path (str): Directory path to validate.

        Raises:
            ValueError: If the directory doesn't exist or is not accessible.
        """
        if not os.path.isdir(path):
            raise ValueError(f"cd: {path}: No such directory")
        if not os.access(path, os.X_OK):
            raise ValueError(f"cd: {path}: Permission denied")


# Register the safe `cd` app
AppRegistry.register("cd", CdApp)
