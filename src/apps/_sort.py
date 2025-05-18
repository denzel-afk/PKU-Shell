"""
Unsafe wrapper for SortApp that suppresses exceptions.

Registers `_sort` command in the AppRegistry.
This version catches all exceptions
and returns error messages as strings,
ensuring that sort failures (e.g., wrong flags,
missing files) don't break shell pipelines or sequences.
"""

from apps.sort import SortApp
from apps.registry import AppRegistry


class _SortApp(SortApp):
    """
    Unsafe version of SortApp that catches exceptions.

    Converts errors (such as invalid arguments or missing files)
    into output strings, allowing the shell to continue
    execution without interruption.
    """

    def run(self, args, stdin=None):
        """
        Execute the _sort application with error suppression.

        Args:
            args (list): Command-line arguments for sort
            (e.g., file names, flags).
            stdin (str, optional): Input from previous command or pipe.

        Returns:
            str: Sorted output or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _sort app
AppRegistry.register("_sort", _SortApp)
