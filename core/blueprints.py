import importlib
import os
import pkgutil
from flask import Blueprint, Flask

def register_all_blueprints(app: Flask):
    """
    Scans the root project directory for domain modules,
    automatically imports them, and registers any Flask Blueprints.
    """
    # Get the root directory of the application
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Core system directories to ignore while scanning for domain modules
    ignored_folders = {"core", "migrations", "tests"}

    # Iterate through all subdirectories in your project root
    for _, module_name, is_pkg in pkgutil.iter_modules([root_dir]):
        if is_pkg and module_name not in ignored_folders:
            try:
                # Dynamically import the domain package (e.g., 'import users')
                domain_package = importlib.import_module(module_name)

                # Scan the public variables inside the package's __init__.py
                for attribute_name in dir(domain_package):
                    attribute = getattr(domain_package, attribute_name)

                    # If it's a Flask Blueprint, register it automatically!
                    if isinstance(attribute, Blueprint):
                        print("Registering blueprint", attribute)
                        app.register_blueprint(attribute)

            except ImportError as err:
                app.logger.error(f"Failed to auto-register domain '{module_name}': {err}")
