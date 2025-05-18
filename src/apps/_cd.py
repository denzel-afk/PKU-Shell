"""
Unsafe wrapper for CdApp that suppresses exceptions.

Registers `_cd` command in the AppRegistry. Unlike the safe `cd` app,
this version catches all exceptions and returns error messages as strings
instead of raising them. This allows command sequences to proceed
even when directory changes fail.
"""

from apps.cd import CdApp
from apps.registry import AppRegistry


class _CdApp(CdApp):
    """
    Unsafe version of CdApp that catches exceptions.

    Overrides the run method to return errors as output instead of raising,
    so the shell does not terminate or clear output on failure.
    """

    def run(self, args, stdin=None):
        """
        Execute the _cd application with error suppression.

        Args:
            args (list): Directory path to change to.
            stdin (str, optional): Unused, included for interface
            compatibility.

        Returns:
            str: Empty string if successful, or error message as string.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _cd app
AppRegistry.register("_cd", _CdApp)
