"""
Module: process_api_call

This module provides a class for processing API calls to fetch and process sun times data.

Classes:
    - ProcessAPICall: A class that handles the process of fetching sun times data from an API, 
      formatting it, adjusting dates, and calculating midday periods.

Usage:
    The `ProcessAPICall` class provides a static method to process API calls and return a structured 
    `SunTimes` object containing the processed sun times data.

Dependencies:
    - app.sun_times: Contains `SunTimes` class used to structure the parsed and processed time data.
    - .process_response_utils.response_handler: Contains the `ResponseHandler` class for handling 
       API responses.
    - .process_response_utils.midday_calculator: Contains the `MiddayPeriodCalculator` class for 
       calculating midday periods.
    - .process_response_utils.date_adjustment: Contains `DateAdjustment` class for adjusting dates.
    - .process_response_utils.sun_times_api: Contains the `SunTimesAPI` class for fetching sun times
       data from an API.
"""

from app.sun_times import SunTimes
from .process_response_utils.response_handler import ResponseHandler
from .process_response_utils.midday_calculator import MiddayPeriodCalculator
from .process_response_utils.date_adjustment import DateAdjustment


class ProcessAPICall:
    """
    A class that handles the process of fetching sun times data from an API, validating it,
    and processing it into a SunTimes object.

    This class provides methods to instantiate necessary components and process API calls
    to return a structured `SunTimes` object containing the processed sun times data.

    Single responsibility: Process API calls to fetch and process sun times data.
    """

    def __init__(self):
        """
        Initializes the necessary components for processing API calls.
        """
        self.response_handler = ResponseHandler()
        self.sun_times_builder = SunTimes()
        self.midday_calculator = MiddayPeriodCalculator()
        self.date_adjustment = DateAdjustment()

    def validate_response(self, response) -> bool:
        """
        Validates the API response to ensure it contains the expected data.

        Args:
            response (dict): The API response containing sun times data.

        Returns:
            bool: True if the response is valid, False otherwise.

        Single Responsibility: Validate the API response format and content.
        """
        required_keys = [
            "sunrise",
            "sunset",
            "civil_twilight_begin",
            "civil_twilight_end",
        ]
        print(response.json)
        for key in required_keys:
            if key not in response.json()["results"]:
                raise RuntimeError(f"Invalid API response format: '{key}' key missing")

    def process_api_call(self, response) -> SunTimes:
        """
        Processes an API call to fetch and process sun times data.

        Args:
            response (dict): The API response containing sun times data.

        Returns:
            SunTimes: A structured object containing the processed sun times data.

        Process:
            1. Handles the API response using `ResponseHandler`.
            2. Processes the raw sun times data using `SunTimes`.
            3. Adjusts the dates using `DateAdjustment`.
            4. Calculates the midday period using `MiddayPeriodCalculator`.

        Single Responsibility: Manage the entire process of fetching and processing sun times data.
        """
        self.validate_response(response)

        formatted_response = self.response_handler.handle_response(response)
        raw_sun_times_object = self.sun_times_builder.process_sun_times(
            formatted_response
        )
        date_adjusted_sun_times_object = self.date_adjustment.adjust_dates(
            raw_sun_times_object
        )
        processed_sun_times_object = self.midday_calculator.process_midday_period(
            date_adjusted_sun_times_object
        )

        return processed_sun_times_object
