"""
Module: sun_times_api

This module provides a class for fetching sun times data from an external API.

Classes:
    - SunTimesAPI: A class that provides a static method to fetch sun times data based on latitude 
      and longitude.

Usage:
    The `SunTimesAPI` class provides a static method to make an API call and retrieve sun times 
    data.

Example:
    response = SunTimesAPI.fetch_sun_times(lat, lng)

Dependencies:
    - requests: Used for handling HTTP requests and responses.
    - flask: Used for accessing the current application configuration.
"""

import requests
from flask import current_app, request


class SunTimesAPI:
    """
    A class that provides methods to fetch sun times data from an external API and construct the
    API URL.

    This class is responsible for constructing the API URL using latitude and longitude, making the
    HTTP GET request, and returning the API response.

    Single responsibility: Fetch sun times data from an external API.
    """

    @staticmethod
    def get_args() -> tuple:
        """
        Gets the latitude and longitude arguments from the user request.

        Returns:
            lat (float): The latitude for the API call.
            lng (float): The longitude for the API call

        Single Responsibility: Get the user's provided latitude and longitude
        """
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)
        return lat, lng

    @staticmethod
    def construct_api_url(lat: float, lng: float) -> str:
        """
        Constructs the API URL using latitude and longitude.

        Args:
            lat (float): The latitude for the API call.
            lng (float): The longitude for the API call.

        Returns:
            str: The constructed API URL.

        Single Responsibility: Construct the API URL for fetching sun times data.
        """
        return f"{current_app.config['SUNRISE_SUNSET_API_BASE_URL']}lat={lat}&lng={lng}"

    @staticmethod
    def fetch_sun_times() -> requests.models.Response:
        """
        Fetches sun times data from an external API based on latitude and longitude.

        Returns:
            requests.models.Response: The raw HTTP response from the API.

        Single Responsibility: Make an API call to fetch sun times data.
        """
        lat, lng = SunTimesAPI.get_args()
        url = SunTimesAPI.construct_api_url(lat, lng)
        response = requests.get(url, timeout=20)
        return response
