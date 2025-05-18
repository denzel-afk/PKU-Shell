"""
Implementation of the `echo` shell application for PKU Shell.

Prints all command-line arguments separated by spaces followed by a newline.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry


class EchoApp(BaseApp):
    """
    Application that mimics the behavior of the Unix `echo` command.

    Outputs arguments separated by spaces followed by a newline.
    Ignores any stdin input.
    """

    def run(self, args, stdin=None):
        """
        Execute the echo command.

        Args:
            args (List[str]): Strings to be echoed.
            stdin (str, optional): Ignored for echo.

        Returns:
            str: Arguments joined with spaces and ending with a newline.
        """
        return " ".join(args) + "\n"


# Register the safe `echo` app
AppRegistry.register("echo", EchoApp)
