"""
Implementation of the 'ls' command for PKU Shell.

Lists non-hidden files and directories in the given path.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry
import os


class LsApp(BaseApp):
    """
    LsApp implements the 'ls' command.

    - If no arguments are provided, it lists the contents of the current
    directory.
    - If a single path is provided, it lists the contents of that path.
    - Ignores hidden files (those starting with '.').
    """

    def run(self, args, stdin=None):
        """
        Execute the 'ls' command.

        Args:
            args (List[str]): A list containing at most one directory path.
            stdin (str, optional): Ignored for this command.

        Returns:
            str: Tab-separated list of visible files/directories.

        Raises:
            ValueError: For incorrect arguments or invalid paths.
        """
        if len(args) > 1:
            raise ValueError("ls: wrong number of command line arguments")

        path = args[0] if args else os.getcwd()

        if not isinstance(path, str) or not path.strip():
            raise ValueError("ls: path cannot be empty or invalid")

        if not os.path.isdir(path):
            raise ValueError(f"ls: cannot access '{path}': No such directory")

        result = []
        try:
            for item in os.listdir(path):
                if not item.startswith("."):
                    result.append(item)
        except PermissionError:
            raise ValueError(f"ls: cannot access '{path}': Permission denied")
        except Exception as e:
            raise ValueError(f"ls: an unexpected error occurred: {str(e)}")

        return "\t".join(result) + "\n"


AppRegistry.register("ls", LsApp)
