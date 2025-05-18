"""
Unsafe wrapper for HeadApp that suppresses exceptions.

Registers `_head` command in the AppRegistry. This version of the head app
catches all exceptions and returns error messages as string output,
allowing pipeline execution to continue even when head fails.
"""

from apps.head import HeadApp
from apps.registry import AppRegistry


class _HeadApp(HeadApp):
    """
    Unsafe version of HeadApp that catches exceptions.

    Converts errors to output strings to prevent crashes or pipeline
    interruption.
    Useful for testing and robust execution.
    """

    def run(self, args, stdin=None):
        """
        Execute the _head application with error suppression.

        Args:
            args (list): Arguments like -n or file paths.
            stdin (str, optional): Input string when reading from pipeline.

        Returns:
            str: First n lines or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _head app
AppRegistry.register("_head", _HeadApp)
