"""
Uniq application for PKU Shell.

Removes adjacent duplicate lines from input.
Supports case-insensitive comparison via the '-i' flag.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class UniqApp(BaseApp):
    """
    Implements the `uniq` command for PKU Shell.

    Features:
    - Removes adjacent duplicate lines
    - Supports `-i` flag for case-insensitive comparison
    """

    def run(self, args, stdin=None):
        """
        Execute the uniq application.

        Args:
            args (List[str]): Command-line arguments.
            stdin (str, optional): Input string from pipe or redirection.

        Returns:
            str: Output with adjacent duplicates removed.
        """
        options, file = self.parse_args(args)
        lines = self.read_input(file, stdin)
        return self.process_uniq(lines, options)

    def parse_args(self, args):
        """
        Parse command-line arguments for `uniq`.

        Returns:
            tuple: (options dict, input file path or None)

        Raises:
            ValueError: If invalid or excessive arguments are passed.
        """
        ignore_case = False
        file = None

        if not args:
            return {"ignore_case": False}, None

        if args[0] == "-i":
            ignore_case = True
            if len(args) > 2:
                raise ValueError(
                    "uniq: wrong number of command line arguments or flags"
                )
            file = args[1] if len(args) == 2 else None

        elif args[0].startswith("-"):
            raise ValueError("uniq: wrong flags")

        elif len(args) == 1:
            file = args[0]

        else:
            raise ValueError(
                "uniq: wrong number of command line arguments or flags"
            )

        return {"ignore_case": ignore_case}, file

    def read_input(self, file, stdin):
        """
        Read input from a file or stdin.

        Returns:
            List[str]: Lines of input.

        Raises:
            ValueError: If file doesn't exist or no input is provided.
        """
        if file:
            try:
                with open(file, "r") as f:
                    return f.readlines()
            except FileNotFoundError:
                raise ValueError(f"uniq: {file}: No such file")
            except PermissionError:
                raise ValueError(f"uniq: {file}: Permission denied")

        elif stdin:
            return stdin.splitlines(keepends=True)

        else:
            raise ValueError("uniq: missing input")

    def process_uniq(self, lines, options):
        """
        Process the lines to remove adjacent duplicates.

        Args:
            lines (List[str]): Input lines.
            options (dict): Options parsed from CLI.

        Returns:
            str: Filtered output string.
        """
        ignore_case = options.get("ignore_case", False)
        result = []
        prev_line = None

        for line in lines:
            comp_line = line.strip()
            if ignore_case:
                if prev_line is None or comp_line.lower() != prev_line.lower():
                    result.append(line)
            else:
                if prev_line is None or comp_line != prev_line:
                    result.append(line)
            prev_line = comp_line

        return "".join(result)


AppRegistry.register("uniq", UniqApp)
