"""
Implementation of the 'pwd' command for PKU Shell.

Returns the current working directory.
"""

from apps.base import BaseApp
from apps.registry import AppRegistry
import os


class PwdApp(BaseApp):
    """
    PwdApp implements the 'pwd' command.

    - Returns the absolute path of the current working directory.
    - Does not accept any arguments.
    """

    def run(self, args, stdin=None):
        """
        Execute the 'pwd' command.

        Args:
            args (List[str]): Must be empty; 'pwd' takes no arguments.
            stdin (str, optional): Ignored.

        Returns:
            str: The current working directory followed by a newline.

        Raises:
            ValueError: If any arguments are provided.
        """
        if args:
            raise ValueError("pwd: too many arguments")
        return os.getcwd() + "\n"


AppRegistry.register("pwd", PwdApp)
