"""Flask Application Factory Module

This module contains the application factory function for creating and
configuring a Flask application instance. It sets up the application with
the appropriate configuration and registers all necessary routes.

Dependencies:
    - Flask
    - .config (local module for get_config method)
    - .routes (local module for containing register_routes method)
"""

from flask import Flask
from .routes import register_routes


def create_app() -> Flask:
    """Create and configure an instance of the Flask application.

    Initializes a new Flask app, loads the appropriate configuration, registers all routes, and
    returns the configured app.

    Returns:
        Flask: A configured Flask application instance ready to run.
    """
    # Initialize the Flask application
    app = Flask(__name__)

    # Load the configuration (prod or dev) for the app
    app.config.from_pyfile("../config.py")
    print(app.config["PROFILE"])

    # Register all routes with the application
    register_routes(app)

    return app
