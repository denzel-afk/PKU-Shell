"""
Implementation of the `grep` shell application for PKU Shell.

Searches for lines matching a regular expression in files or stdin input.
"""

import re
from apps.base import BaseApp
from apps.registry import AppRegistry


class GrepApp(BaseApp):
    """
    Application that replicates the behavior of the Unix `grep` command.

    Supports regular expression matching in file contents or standard input.
    """

    def run(self, args, stdin=None):
        """
        Execute the grep command.

        Args:
            args (List[str]):
                First argument is the regex pattern; the rest are filenames.
            stdin (str, optional):
                Optional input string (used when no file is provided).

        Returns:
            str:
                Lines matching the pattern, optionally prefixed with filenames.

        Raises:
            ValueError:
                If pattern is missing or files are not found.
        """
        if not args:
            raise ValueError("grep: no input provided")

        pattern = args[0]
        files = args[1:]

        try:
            regex_pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"grep: invalid regular expression: {e}")

        if not files:
            if stdin is None:
                raise ValueError("grep: no input provided")
            return self.search_stdin(stdin, regex_pattern)

        return self.search_files(files, regex_pattern)

    def search_files(self, files, regex_pattern):
        """
        Search for matches in the given list of files.

        Args:
            files (List[str]): List of file paths to search in.
            regex_pattern (re.Pattern): Compiled regex pattern.

        Returns:
            str: Matching lines, possibly prefixed with filenames.
        """
        result = []
        for file in files:
            try:
                with open(file, "r") as f:
                    for line in f:
                        if regex_pattern.search(line):
                            match = (
                                f"{file}:{line.strip()}"
                                if len(files) > 1
                                else line.strip()
                            )
                            result.append(match)
            except FileNotFoundError:
                raise ValueError(f"grep: {file}: No such file")
        return "\n".join(result) if result else ""

    def search_stdin(self, input_data, regex_pattern):
        """
        Search for matches in stdin input.

        Args:
            input_data (str): Input lines separated by newlines.
            regex_pattern (re.Pattern): Compiled regex pattern.

        Returns:
            str: Matching lines from stdin.
        """
        result = [
            line for line in input_data.splitlines()
            if regex_pattern.search(line)
        ]
        return "\n".join(result) if result else ""


# Register the safe `grep` app
AppRegistry.register("grep", GrepApp)
