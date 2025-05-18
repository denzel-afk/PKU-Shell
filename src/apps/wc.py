"""
Word Count (wc) application for PKU Shell.

Counts the number of lines, words, and characters in a file or standard input.
Supports flags:
  -l : count lines
  -w : count words
  -m : count characters
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class WcApp(BaseApp):
    """
    Implements the `wc` command.

    Features:
    - Counts lines (-l), words (-w), and characters (-m)
    - Accepts file input or stdin
    """

    def run(self, args, stdin=None):
        """
        Execute the wc application.

        Args:
            args (List[str]): Command-line arguments.
            stdin (str, optional): Input string if piped or redirected.

        Returns:
            str: Formatted counts based on specified flags.
        """
        options, files = self.parse_arguments(args)

        if not any(options.values()):
            options = {"lines": True, "words": True, "chars": True}

        content = self.get_input(files, stdin)
        counts = self.count_content(content)
        output = self.format_output(counts, options)
        return output.strip() if output else ""

    def parse_arguments(self, args):
        """
        Parse wc command-line flags and filenames.

        Args:
            args (List[str]): Argument list.

        Returns:
            Tuple[dict, List[str]]: Parsed options and file list.

        Raises:
            ValueError: If invalid option is encountered.
        """
        options = {"lines": False, "words": False, "chars": False}
        files = []

        for arg in args:
            if arg == "-l":
                options["lines"] = True
            elif arg == "-w":
                options["words"] = True
            elif arg == "-m":
                options["chars"] = True
            elif arg.startswith("-"):
                raise ValueError(f"wc: invalid option -- '{arg}'")
            else:
                files.append(arg)

        return options, files

    def get_input(self, files, stdin):
        """
        Read input from specified files or stdin.

        Args:
            files (List[str]): Filenames to read from.
            stdin (str): Piped input.

        Returns:
            str: Combined input content.

        Raises:
            ValueError: If file not found or no input is provided.
        """
        if files:
            data = []
            for file in files:
                try:
                    with open(file, "r") as f:
                        data.append(f.read())
                except FileNotFoundError:
                    raise ValueError(f"wc: {file}: No such file")
            return "\n".join(data)
        elif stdin is not None:
            return stdin
        else:
            raise ValueError("wc: no input provided")

    def count_content(self, content):
        """
        Count lines, words, and characters in the input.

        Args:
            content (str): The content to analyze.

        Returns:
            dict: Counts for 'lines', 'words', and 'chars'.
        """
        return {
            "lines": content.count("\n"),
            "words": len(content.split()),
            "chars": len(content)
        }

    def format_output(self, counts, options):
        """
        Format the output based on enabled flags.

        Args:
            counts (dict): Counted values.
            options (dict): Flags indicating which counts to show.

        Returns:
            str: Formatted result string.
        """
        result = []
        if options["lines"]:
            result.append(str(counts["lines"]))
        if options["words"]:
            result.append(str(counts["words"]))
        if options["chars"]:
            result.append(str(counts["chars"]))
        return " ".join(result)


AppRegistry.register("wc", WcApp)
