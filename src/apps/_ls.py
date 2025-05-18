"""
Unsafe wrapper for LsApp that suppresses exceptions.

Registers `_ls` command in the AppRegistry. This version catches all exceptions
and returns error messages as output strings, so that shell pipelines
or sequences can continue even if directory listing fails.
"""

from apps.ls import LsApp
from apps.registry import AppRegistry


class _LsApp(LsApp):
    """
    Unsafe version of LsApp that catches exceptions.

    Errors like 'No such directory' are returned as string output instead of
    crashing the shell or stopping the pipeline.
    """

    def run(self, args, stdin=None):
        """
        Execute the _ls application with error suppression.

        Args:
            args (list): File or directory names to list.
            stdin (str, optional): Ignored by ls; included for compatibility.

        Returns:
            str: Directory listing or error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _ls app
AppRegistry.register("_ls", _LsApp)
