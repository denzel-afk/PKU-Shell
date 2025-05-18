"""
Unsafe wrapper for CatApp that suppresses exceptions.

Registers `_cat` command in the AppRegistry. Unlike the safe `cat` app,
this version catches all exceptions and returns error messages as strings
instead of raising them. This allows pipelines and command sequences
to continue even if file errors occur.
"""

from apps.cat import CatApp
from apps.registry import AppRegistry


class _CatApp(CatApp):
    """
    Unsafe version of CatApp that catches exceptions.

    Overrides the run method to return errors as output instead of raising,
    enabling the shell to proceed without interruption.
    """

    def run(self, args, stdin=None):
        """
        Execute the _cat application with error suppression.

        Args:
            args (list): List of file paths or arguments to read.
            stdin (str, optional): Input string to read from.

        Returns:
            str: Output from files or error message as string.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _cat app
AppRegistry.register("_cat", _CatApp)
