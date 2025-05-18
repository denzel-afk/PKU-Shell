"""
Unsafe wrapper for TailApp that suppresses exceptions.

Registers `_tail` command in the AppRegistry.
This unsafe version catches all exceptions
and returns error messages as output strings,
enabling continuation of pipelines or
command sequences even when tail encounters errors
(e.g., missing files or bad flags).
"""

from apps.tail import TailApp
from apps.registry import AppRegistry


class _TailApp(TailApp):
    """
    Unsafe version of TailApp that catches exceptions.

    Ensures the shell remains stable by converting execution
    errors into output strings.
    Useful for fault-tolerant pipeline execution and testing.
    """

    def run(self, args, stdin=None):
        """
        Execute the _tail application with error suppression.

        Args:
            args (list): Arguments for tail (e.g., -n, file paths).
            stdin (str, optional): Input from a pipeline or heredoc.

        Returns:
            str: Output of the last n lines or an error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _tail app
AppRegistry.register("_tail", _TailApp)
