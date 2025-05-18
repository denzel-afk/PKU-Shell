"""
Application registry for PKU Shell.

This module maintains a global registry of available shell applications,
mapping command names to their corresponding class implementations.
"""

from typing import Dict, Type
from apps.base import BaseApp


class AppRegistry:
    """
    Registry for shell applications.

    This class maps command names (e.g., 'echo', 'cat') to their corresponding
    application classes (subclasses of BaseApp). It supports dynamic
    registration and lookup of applications.
    """

    _registry: Dict[str, Type[BaseApp]] = {}

    @classmethod
    def register(cls, name: str, app_cls: Type[BaseApp]):
        """
        Register an application under a given command name.

        Args:
            name (str): The shell command name (e.g., 'echo', '_cat').
            app_cls (Type[BaseApp]): The class that implements the application.
        """
        cls._registry[name] = app_cls

    @classmethod
    def get(cls, name: str) -> BaseApp:
        """
        Retrieve an application instance by command name.

        Args:
            name (str): The shell command name.

        Returns:
            BaseApp: An instance of the corresponding application class.

        Raises:
            Exception: If the command name is not registered.
        """
        if name not in cls._registry:
            raise Exception(f"Unknown command: {name}")
        return cls._registry[name]()
