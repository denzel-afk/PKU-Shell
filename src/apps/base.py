"""
Base interface for all shell applications (apps) in PKU Shell.

Defines the common structure for application execution, including:
- Standardized `run` method
- Optional `stdin` support
- Utility method to identify unsafe variants (prefixed with '_')
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class BaseApp(ABC):
    """
    Abstract base class for all shell applications.

    All apps must implement the `run` method, which defines how the app behaves
    given a list of arguments and optional standard input.
    """

    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def run(self, args: List[str], stdin: Optional[str] = None) -> str:
        """
        Run the application.

        Args:
            args (List[str]): Command-line arguments.
            stdin (Optional[str]): Input string from pipe or redirection.

        Returns:
            str: Output string produced by the application.
        """
        ...

    def is_unsafe(self) -> bool:
        """
        Check whether the app is an unsafe variant.

        Returns:
            bool: True if the app name starts with an underscore
            (e.g., _cat), False otherwise.
        """
        return self.name.startswith("_")
