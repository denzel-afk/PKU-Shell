"""
Unsafe wrapper for UniqApp that suppresses exceptions.

Registers `_uniq` command in the AppRegistry. This version catches
all exceptions and returns error messages as strings,
so pipelines or command sequences continue even when uniq encounters
invalid input or too many arguments.
"""

from apps.uniq import UniqApp
from apps.registry import AppRegistry


class _UniqApp(UniqApp):
    """
    Unsafe version of UniqApp that catches exceptions.

    Converts runtime errors into output strings to avoid
    interrupting execution flow.
    Useful for robustness during testing or complex shell operations.
    """

    def run(self, args, stdin=None):
        """
        Execute the _uniq application with error suppression.

        Args:
            args (list): Arguments to uniq (e.g., filename, -i).
            stdin (str, optional): Input stream from pipe or heredoc.

        Returns:
            str: Deduplicated output or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _uniq app
AppRegistry.register("_uniq", _UniqApp)
