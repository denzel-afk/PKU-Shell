"""
Tail application for PKU Shell.

Returns the last N lines of input from a file or stdin.
Supports the '-n' flag to specify number of lines.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class TailApp(BaseApp):
    """
    Implements the `tail` command for PKU Shell.

    Features:
    - Reads from file or stdin
    - Supports `-n` flag for custom line count
    """

    def run(self, args, stdin=None):
        """
        Execute the tail application.

        Args:
            args (List[str]): Command-line arguments.
            stdin (str, optional): Input string if piped or redirected.

        Returns:
            str: Last N lines of the input.
        """
        if not args and stdin:
            lines = self.read_input(None, stdin)
            return self.get_tail(lines, 10)

        num_lines, file = self.parse_args(args)
        lines = self.read_input(file, stdin)
        return self.get_tail(lines, num_lines)

    def parse_args(self, args):
        """
        Parse command-line arguments.

        Returns:
            tuple: (number of lines, file path)

        Raises:
            ValueError: On invalid or missing arguments.
        """
        num_lines = 10
        file = None

        if not args:
            raise ValueError("tail: no input provided")
        elif len(args) == 1:
            file = args[0]
        elif len(args) == 3 and args[0] == "-n":
            try:
                num_lines = int(args[1])
                if num_lines < 0:
                    raise ValueError("tail: invalid number of lines")
            except ValueError:
                raise ValueError("tail: invalid number of lines")
            file = args[2]
        elif len(args) >= 2 and args[0].startswith("-"):
            raise ValueError("tail: wrong flags")
        else:
            raise ValueError(
                "tail: wrong number of command line arguments or flags"
            )

        return num_lines, file

    def read_input(self, file, stdin):
        """
        Read lines from file or stdin.

        Returns:
            List[str]: Input lines.

        Raises:
            ValueError: If file is missing, unreadable, or inaccessible.
        """
        if file:
            try:
                with open(file, "r") as f:
                    return f.readlines()
            except FileNotFoundError:
                raise ValueError(f"tail: {file}: No such file")
            except PermissionError:
                raise ValueError(f"tail: {file}: Permission denied")
        elif stdin:
            return stdin.splitlines(keepends=True)
        else:
            raise ValueError("tail: no input provided")

    def get_tail(self, lines, num_lines):
        """
        Get the last N lines from the input.

        Returns:
            str: Tail of the input.
        """
        if num_lines == 0:
            return ""
        return "".join(lines[-num_lines:])


AppRegistry.register("tail", TailApp)
