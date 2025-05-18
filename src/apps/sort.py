"""
Sort application for PKU Shell.

Supports sorting lines from files or standard input with
optional reverse ordering.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class SortApp(BaseApp):
    """
    Implements the `sort` command.

    Supports:
    - Reading from file or stdin
    - Sorting in ascending (default) or descending (-r) order
    """

    def run(self, args, stdin=None):
        """
        Execute the sort application.

        Args:
            args (List[str]): Command-line arguments, e.g., ['-r', 'file.txt']
            stdin (str, optional): Input from a pipeline or redirection

        Returns:
            str: Sorted text
        """
        options, file = self.parse_args(args)
        lines = self.read_input(file, stdin)
        return self.process_sort(lines, options)

    def parse_args(self, args):
        """
        Parse command-line arguments.

        Supports '-r' for reverse sorting.

        Returns:
            tuple: ({'reverse': bool}, file_path or None)
        """
        reverse = False
        file = None

        if not args:
            return {"reverse": False}, None

        if args[0] == "-r":
            reverse = True
            if len(args) > 2:
                raise ValueError(
                    "sort: wrong number of command line arguments"
                )
            file = args[1] if len(args) == 2 else None

        elif args[0].startswith("-"):
            raise ValueError(f"sort: unknown option {args[0]}")

        elif len(args) == 1:
            file = args[0]

        else:
            raise ValueError("sort: wrong number of command line arguments")

        return {"reverse": reverse}, file

    def read_input(self, file, stdin):
        """
        Read input from file or stdin.

        Returns:
            List[str]: List of input lines

        Raises:
            ValueError: If file is missing or unreadable
        """
        if file:
            try:
                with open(file, "r") as f:
                    return f.readlines()
            except FileNotFoundError:
                raise ValueError(f"sort: {file}: No such file")
            except PermissionError:
                raise ValueError(f"sort: {file}: Permission denied")
        elif stdin:
            return stdin.splitlines(keepends=True)
        else:
            raise ValueError("sort: missing input")

    def process_sort(self, lines, options):
        """
        Sort the input lines.

        Args:
            lines (List[str]): Lines to sort
            options (dict): Options dictionary

        Returns:
            str: Sorted result as a single string
        """
        reverse = options.get("reverse", False)
        sorted_lines = sorted(lines, reverse=reverse)
        return "".join(sorted_lines)


AppRegistry.register("sort", SortApp)
