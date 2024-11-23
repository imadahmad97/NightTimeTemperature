Module NightTimeTemperature.app
===============================
Flask Application Factory Module

This module contains the application factory function for creating and
configuring a Flask application instance. It sets up the application with
the appropriate configuration and registers all necessary routes.

Dependencies:
    - Flask
    - .config (local module for get_config method)
    - .routes (local module for containing register_routes method)

Sub-modules
-----------
* NightTimeTemperature.app.calculate_temp
* NightTimeTemperature.app.main
* NightTimeTemperature.app.process_response
* NightTimeTemperature.app.routes
* NightTimeTemperature.app.sun_times

Functions
---------

`create_app() ‑> flask.app.Flask`
:   Create and configure an instance of the Flask application.
    
    Initializes a new Flask app, loads the appropriate configuration, registers all routes, and
    returns the configured app.
    
    Returns:
        Flask: A configured Flask application instance ready to run.