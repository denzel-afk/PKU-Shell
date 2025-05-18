"""
Unsafe wrapper for GrepApp that suppresses exceptions.

Registers `_grep` command in the AppRegistry. This version catches
all exceptions and returns error messages as strings, allowing
the shell to continue execution even if grep fails due to invalid
input or missing files.
"""

from apps.grep import GrepApp
from apps.registry import AppRegistry


class _GrepApp(GrepApp):
    """
    Unsafe version of GrepApp that catches exceptions.

    Useful for testing and pipelines where grep failures
    should not halt execution. Exceptions are returned as
    output instead of being raised.
    """

    def run(self, args, stdin=None):
        """
        Execute the _grep application with error suppression.

        Args:
            args (list): Grep arguments (e.g., patterns, file names).
            stdin (str, optional): Input text to search from
            pipe or redirection.

        Returns:
            str: Matching lines or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _grep app
AppRegistry.register("_grep", _GrepApp)
