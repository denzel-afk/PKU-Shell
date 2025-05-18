"""
Implementation of the `cut` shell application for PKU Shell.

Supports byte-range selection using the `-b` option.
Allows reading from files or standard input (stdin).
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class CutApp(BaseApp):
    """
    Application that implements the behavior of the Unix `cut` command.

    Supports byte-wise selection using the `-b` option with
    flexible range syntax.
    """

    def parse_byte_ranges(self, ranges):
        """
        Parse a comma-separated string of byte ranges into tuples.

        Args:
            ranges (str): Byte ranges (e.g., '1-3,5,7-', '-4').

        Returns:
            List[Tuple[int, int]]: Normalized list of
            (start, end) byte positions.

        Raises:
            ValueError: If range format is invalid.
        """
        byte_ranges = []
        for r in ranges.split(','):
            if r.startswith('-'):
                try:
                    end = int(r[1:]) - 1
                    byte_ranges.append((0, end))
                except ValueError:
                    raise ValueError(f"cut: invalid range {r}")
            elif r.endswith('-'):
                try:
                    start = int(r[:-1]) - 1
                    byte_ranges.append((start, float('inf')))
                except ValueError:
                    raise ValueError(f"cut: invalid range {r}")
            elif '-' in r:
                try:
                    start, end = map(int, r.split('-'))
                    byte_ranges.append((start - 1, end - 1))
                except ValueError:
                    raise ValueError(f"cut: invalid range {r}")
            else:
                try:
                    start = int(r) - 1
                    byte_ranges.append((start, start))
                except ValueError:
                    raise ValueError(f"cut: invalid range {r}")

        # Merge overlapping/adjacent ranges
        byte_ranges.sort()
        merged_ranges = []
        for start, end in byte_ranges:
            if not merged_ranges or merged_ranges[-1][1] < start - 1:
                merged_ranges.append((start, end))
            else:
                merged_start, merged_end = merged_ranges.pop()
                merged_ranges.append((merged_start, max(merged_end, end)))

        return merged_ranges

    def read_input(self, file, stdin):
        """
        Read lines from a file or from stdin.

        Args:
            file (str): Path to file (optional).
            stdin (str): Standard input string.

        Returns:
            List[str]: List of input lines.

        Raises:
            ValueError: If file is missing or unreadable.
        """
        if file:
            try:
                with open(file, 'r') as f:
                    return f.readlines()
            except FileNotFoundError:
                raise ValueError(f"cut: {file}: No such file")
        elif stdin:
            return stdin.splitlines()
        else:
            raise ValueError("cut: no input provided")

    def cut_lines(self, lines, byte_ranges):
        """
        Apply byte-range extraction on each line.

        Args:
            lines (List[str]): Input lines.
            byte_ranges (List[Tuple[int, int]]): Parsed byte ranges.

        Returns:
            List[str]: Resulting lines after cutting.
        """
        result = []
        for line in lines:
            cut_line = ''
            for start, end in byte_ranges:
                if end == float('inf'):
                    end = len(line) - 1
                start = max(0, start)
                end = min(len(line) - 1, end)
                if start <= end:
                    cut_line += line[start:end + 1]
            result.append(cut_line.rstrip("\n") if cut_line else "")
        return result

    def run(self, args, stdin=None):
        """
        Execute the cut command with `-b` option only.

        Args:
            args (List[str]): Arguments passed to cut.
            stdin (str, optional): Input from pipeline or redirection.

        Returns:
            str: Processed string output.

        Raises:
            ValueError: If required args are missing or invalid.
        """
        if len(args) < 2:
            raise ValueError("cut: missing required arguments")

        option = args[0]
        if not option.startswith("-b"):
            raise ValueError("cut: invalid option")

        byte_ranges = self.parse_byte_ranges(args[1])
        lines = self.read_input(args[2] if len(args) > 2 else None, stdin)
        if not lines:
            return ""
        result = self.cut_lines(lines, byte_ranges)
        return "\n".join(result) + ("\n" if result else "")


# Register the safe `cut` app
AppRegistry.register("cut", CutApp)
