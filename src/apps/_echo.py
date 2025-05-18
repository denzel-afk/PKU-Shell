"""
Unsafe wrapper for EchoApp that suppresses exceptions.

Registers `_echo` command in the AppRegistry.
This version catches all exceptions and returns error messages as
string output instead of raising them.
Useful for testing and ensuring pipeline robustness.
"""

from apps.echo import EchoApp
from apps.registry import AppRegistry


class _EchoApp(EchoApp):
    """
    Unsafe version of EchoApp that catches exceptions.

    Overrides the run method to ensure that any exception is returned as output
    rather than crashing the shell or clearing pipeline output.
    """

    def run(self, args, stdin=None):
        """
        Execute the _echo application with error suppression.

        Args:
            args (list): Words or arguments to echo back.
            stdin (str, optional): Ignored; included for
            interface compatibility.

        Returns:
            str: Echoed string or error message.
        """
        try:
            return super().run(args, stdin)
        except Exception as error:
            return f"{error}\n"


# Register the unsafe _echo app
AppRegistry.register("_echo", _EchoApp)
