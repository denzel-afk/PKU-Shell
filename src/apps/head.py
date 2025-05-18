"""
Implementation of the `head` application for PKU Shell.

Reads and returns the first N lines of a file or standard input.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class HeadApp(BaseApp):
    """
    Simulates the Unix `head` command.

    Supports reading the top lines of files or from standard input,
    with an optional `-n` flag to specify number of lines.
    """

    def run(self, args, stdin=None):
        """
        Execute the head command logic.

        Args:
            args (List[str]): Command-line arguments.
            stdin (str, optional): Input string, used when no file is given.

        Returns:
            str: First N lines of input.

        Raises:
            ValueError: If input is invalid,
            file is missing, or flags are incorrect.
        """
        if not args and stdin:
            lines = self.read_input(None, stdin)
            return self.get_head(lines, 10)

        num_lines, file = self.parse_args(args)
        lines = self.read_input(file, stdin)
        return self.get_head(lines, num_lines)

    def parse_args(self, args):
        """
        Parse arguments and extract number of lines and filename.

        Args:
            args (List[str]): Command-line arguments.

        Returns:
            Tuple[int, str]: Number of lines to read, and filename (if given).

        Raises:
            ValueError: On wrong number of arguments or invalid flags.
        """
        num_lines = 10
        file = None

        if not args:
            raise ValueError("head: no input provided")
        elif len(args) == 1:
            file = args[0]
        elif len(args) == 3 and args[0] == "-n":
            try:
                num_lines = int(args[1])
                if num_lines < 0:
                    raise ValueError("head: invalid number of lines")
            except ValueError:
                raise ValueError("head: invalid number of lines")
            file = args[2]
        elif len(args) >= 2 and args[0].startswith("-"):
            raise ValueError("head: wrong flags")
        else:
            raise ValueError(
                "head: wrong number of command line arguments or flags"
            )

        return num_lines, file

    def read_input(self, file, stdin):
        """
        Read lines from file or stdin.

        Args:
            file (str): File path to read.
            stdin (str): Optional input string.

        Returns:
            List[str]: List of lines from input.

        Raises:
            ValueError: If file is missing or permission is denied.
        """
        if file:
            try:
                with open(file, "r") as f:
                    return f.readlines()
            except FileNotFoundError:
                raise ValueError(f"head: {file}: No such file")
            except PermissionError:
                raise ValueError(f"head: {file}: Permission denied")
        elif stdin:
            return stdin.splitlines(keepends=True)
        else:
            raise ValueError("head: no input provided")

    def get_head(self, lines, num_lines):
        """
        Return the first `num_lines` from the input.

        Args:
            lines (List[str]): Input lines.
            num_lines (int): Number of lines to extract.

        Returns:
            str: Extracted top N lines as a single string.
        """
        return "".join(lines[:num_lines])


# Register the safe app
AppRegistry.register("head", HeadApp)
