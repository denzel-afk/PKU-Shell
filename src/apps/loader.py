"""
Application Loader for PKU Shell.

Automatically discovers and imports all app modules in the `apps/` directory.
Ensures that all command implementations (e.g., cat, echo, grep) are registered
to the AppRegistry upon shell startup.
"""

import os
import importlib


def load_all_apps():
    """
    Dynamically load all Python modules in the apps directory.

    Scans the `apps/` folder and imports all `.py` files
    that are not dunder modules (like `__init__.py`).

    This triggers the registration of each app to the AppRegistry.
    """
    app_dir = os.path.dirname(__file__)
    for filename in os.listdir(app_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"apps.{filename[:-3]}"
            importlib.import_module(module_name)
