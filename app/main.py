"""
Module: main

This module provides the main function for fetching sun times data, processing the API response, 
and calculating the temperature based on the processed data.

Functions:
    - main: Fetches sun times data based on latitude and longitude, processes the API response, 
      and calculates the temperature.

Dependencies:
    - flask: Used for creating JSON responses.
    - .process_response.process_response: Contains the `ProcessAPICall` class for processing API 
       responses.
    - .process_response.process_response_utils.sun_times_api: Contains the `SunTimesAPI` class for 
       fetching sun times data.
    - .calculate_temp.calculate_temp: Contains the `CalculateTemp` class for calculating temperature
       based on processed sun times data.
"""

from flask import jsonify, Response
from app.sun_times import SunTimes
from .process_response.process_response import ProcessAPICall
from .calculate_temp.calculate_temp import CalculateTemp


def main() -> Response:
    """
    Main function to handle one user request end to end, and returning the response.

    Process:
        1. Fetches sun times data using `SunTimesAPI`.
        2. Processes the API response using `ProcessAPICall`.
        3. Calculates the temperature using `CalculateTemp`.

    Single Responsibility: Handles one user request end to end.
    """

    api_processor: ProcessAPICall = ProcessAPICall()
    processed_api_response: SunTimes = api_processor.process_api_call()
    return jsonify(temperature=CalculateTemp.calculate_temp(processed_api_response))
