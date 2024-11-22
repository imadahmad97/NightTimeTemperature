"""
Module: routes

This module provides the route registration function for the Flask application.

Functions:
    - register_routes: Registers the routes for the Flask application, including the route for 
      fetching and processing sun times data to calculate the night-time temperature.

Dependencies:
    - flask: Used for handling HTTP requests and responses.
    - .main: Contains the `main` function for fetching, processing sun times data, and calculating 
      temperature.
"""

from flask import request, Response
from .main import main


def register_routes(app):
    """
    Registers the routes for the Flask application.

    This function sets up the route for fetching and processing sun times data to calculate the
    night-time temperature.

    Args:
        app: The Flask application instance.

    Single Responsibility: Register the necessary routes for the Flask application.
    """

    @app.route("/night-time-temperature", methods=["GET"])
    def night_time_temperature_route() -> Response:
        """
        Route for fetching and processing sun times data to calculate the night-time temperature.

        This route handles GET requests, extracts latitude and longitude from the query parameters,
        and calls the `main` function to fetch, process sun times data, and calculate the
        temperature.

        Returns:
            Response: A JSON response containing the calculated temperature.

        Single Responsibility: Handle the GET request to calculate the night-time temperature.
        """
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)

        return main(lat, lng)
