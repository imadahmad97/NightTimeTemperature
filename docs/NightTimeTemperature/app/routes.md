Module NightTimeTemperature.app.routes
======================================
Module: routes

This module provides the route registration function for the Flask application.

Functions:
    - register_routes: Registers the routes for the Flask application, including the route for 
      fetching and processing sun times data to calculate the night-time temperature.

Dependencies:
    - flask: Used for handling HTTP requests and responses.
    - .main: Contains the `main` function for fetching, processing sun times data, and calculating 
      temperature.

Functions
---------

`register_routes(app)`
:   Registers the routes for the Flask application.
    
    This function sets up the route for fetching and processing sun times data to calculate the
    night-time temperature.
    
    Args:
        app: The Flask application instance.
    
    Single Responsibility: Register the necessary routes for the Flask application.