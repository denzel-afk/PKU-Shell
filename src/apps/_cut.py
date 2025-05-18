"""
Unsafe wrapper for CutApp that suppresses exceptions.

Registers `_cut` command in the AppRegistry. This version of the cut app
catches all exceptions and returns error messages as strings instead
of raising them. This ensures pipelines and command sequences can
continue executing even when errors occur.
"""

from apps.cut import CutApp
from apps.registry import AppRegistry


class _CutApp(CutApp):
    """
    Unsafe version of CutApp that catches exceptions.

    Overrides the run method to return errors as string output instead of
    raising exceptions, preventing the shell from stopping on invalid
    arguments or missing files.
    """

    def run(self, args, stdin=None):
        """
        Execute the _cut application with error suppression.

        Args:
            args (list): Command-line arguments for cut (e.g., -b, files).
            stdin (str, optional): Input from previous command or string.

        Returns:
            str: Extracted output or error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _cut app
AppRegistry.register("_cut", _CutApp)
