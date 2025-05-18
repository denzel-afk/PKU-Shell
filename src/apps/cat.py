"""
Implementation of the `cat` shell application for PKU Shell.

Supports reading content from files or stdin and outputs it to stdout.
Handles multiple file arguments, missing files, and permission
errors gracefully.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class CatApp(BaseApp):
    """
    Application that implements the behavior of the Unix `cat` command.

    - If arguments are provided, it reads and concatenates
    the contents of those files.
    - If no arguments are given but stdin is provided,
    it returns stdin directly.
    - Raises an error if no input source is available.
    """

    def run(self, args, stdin=None):
        """
        Execute the cat command.

        Args:
            args (List[str]): List of filenames to read.
            stdin (str, optional): Input string from pipe or redirection.

        Returns:
            str: Concatenated content from files or stdin.

        Raises:
            ValueError: If no input is provided, file is missing,
            or permission is denied.
        """
        if not args and stdin is None:
            raise ValueError("cat: no input provided")

        output = []
        if args:
            for filename in args:
                output.append(self.read_file(filename))
        elif stdin is not None:
            output.append(stdin)

        return self.combine_output(output)

    def read_file(self, filename):
        """
        Read content from a file with error handling.

        Args:
            filename (str): Path to the file.

        Returns:
            str: Contents of the file.

        Raises:
            ValueError: If the file is not found or permission is denied.
        """
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"cat: {filename}: No such file")
        except PermissionError:
            raise ValueError(f"cat: {filename}: Permission denied")

    def combine_output(self, output):
        """
        Combine the list of outputs into a single string.

        Args:
            output (List[str]): List of strings from files or stdin.

        Returns:
            str: Final output to be returned by cat.
        """
        return "".join(output)


# Register the safe `cat` app
AppRegistry.register("cat", CatApp)
