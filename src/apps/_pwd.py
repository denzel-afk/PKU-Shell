"""
Unsafe wrapper for PwdApp that suppresses exceptions.

Registers `_pwd` command in the AppRegistry. This unsafe version catches
all exceptions and returns error messages as strings, allowing
pipeline and sequence continuation even when the pwd command fails
(e.g., due to too many arguments).
"""

from apps.pwd import PwdApp
from apps.registry import AppRegistry


class _PwdApp(PwdApp):
    """
    Unsafe version of PwdApp that catches exceptions.

    Ensures that any error (e.g., argument misuse) is returned as output
    instead of raising an exception that might break shell flow.
    """

    def run(self, args, stdin=None):
        """
        Execute the _pwd application with error suppression.

        Args:
            args (list): Arguments for pwd (should normally be empty).
            stdin (str, optional): Ignored for pwd; present for
            interface compatibility.

        Returns:
            str: Current working directory or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _pwd app
AppRegistry.register("_pwd", _PwdApp)
