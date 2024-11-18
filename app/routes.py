"""Temperature Service Route Handlers Module.

This module provides Flask route handlers for the NightTimeTemperature API. It includes an endpoint
for getting temperature readings based on geographical coordinates,with support for both production 
and testing environments through mock values.

Endpoints:
    GET /night-time-temperature:
        Retrieves night-time temperature for given coordinates
        Query Parameters:
            lat (float): Latitude coordinate
            lng (float): Longitude coordinate
        Returns:
            JSON with temperature data or error message

Configuration:
    MOCK_VALUES (bool): Configuration flag to enable/disable mock temperature values
                       Used primarily for testing and development environments.

Dependencies:
    - Flask
    - .utils (internal method containing calculate_temp method)
"""

from flask import request, jsonify, current_app
from .utils import calculate_temp


def register_routes(app):
    """Registers Flask route handlers for REST API endpoints.

    This function sets up the REST API endpoint for all routes in the flask API. It includes support
    for mock values during testing/development.

    Args:
        app (Flask): The Flask application instance to register routes with.

    Returns:
        None: Routes are registered directly with the Flask app.
    """

    @app.route("/night-time-temperature", methods=["GET"])
    def get_temperature():
        """Handles GET requests for night-time temperature data.

        Retrieves temperature data for specified coordinates, supporting both
        real calculations and mock values for testing.

        Returns:
            tuple: JSON response with temperature data and status code
                  Format: {"temperature": float} for success
                  Format: {"error": str} for failure
            for example:
            {
            "temperature": 2700
            }

        Raises:
            RuntimeError: If temperature calculation fails
        """
        # Extract coordinate parameters from GET request
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)

        try:
            if current_app.config["MOCK_VALUES"]:
                # Use mock values for testing/development environments
                temperature = calculate_temp(lat, lng)
            else:
                # Calculate actual temperature using external service/calculation
                temperature = calculate_temp(lat, lng)
            # Return successful response with temperature data
            return jsonify(temperature=temperature)
        except RuntimeError as e:
            # Return error response if temperature calculation fails
            return jsonify(error=str(e)), 400
