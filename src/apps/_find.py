"""
Unsafe wrapper for FindApp that suppresses exceptions.

Registers `_find` command in the AppRegistry. Unlike the safe `find` app,
this version catches all exceptions and returns error messages as strings,
allowing pipelines or command sequences to continue even if the search fails.
"""

from apps.find import FindApp
from apps.registry import AppRegistry


class _FindApp(FindApp):
    """
    Unsafe version of FindApp that catches exceptions.

    Useful for handling file lookup errors gracefully in pipelines.
    Converts exceptions into user-readable output instead of halting execution.
    """

    def run(self, args, stdin=None):
        """
        Execute the _find application with error suppression.

        Args:
            args (list): Arguments for the find command
            (e.g., directory, -name).
            stdin (str, optional): Not used for find; kept for
            interface compatibility.

        Returns:
            str: Matched file paths or error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _find app
AppRegistry.register("_find", _FindApp)
