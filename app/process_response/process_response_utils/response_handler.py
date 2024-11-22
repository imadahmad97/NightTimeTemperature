"""
Module: response_handler

This module provides classes and methods for handling API responses from the sunrise-sunset API.

Classes:
    - AbstractResponseHandler: An abstract base class that defines the template for converting API 
      responses into `SunTimes` objects. It includes abstract methods for extracting and parsing 
      time data from the API response.
    - ResponseHandler: A concrete implementation of `AbstractResponseHandler` that provides specific
      methods for extracting and parsing time data from the API response.

Usage:
    The `AbstractResponseHandler` class should be subclassed to create custom response handlers that
    implement the `extract_times_from_api_response` and `parse_sun_times` methods. The 
    `ResponseHandler` class provides one such implementation for handling typical sunrise and sunset
    API responses.

Example:
    response_handler = ResponseHandler()
    sun_times = response_handler.handle_response(api_response)

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for parsing and handling date and time data.
    - typing: Provides type hinting for better code readability and maintenance.
    - requests: Used for handling HTTP requests and responses.
    - app.sun_times: Contains the `SunTimes` class used to structure the parsed time data.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
import requests
from app.sun_times import SunTimes


class AbstractResponseHandler(ABC):
    """
    Abstract base class for converting API responses into SunTime Objects.

    This class provides a template for response handlers by defining:
    - A method to extract raw time data from the API response.
    - A method to parse the extracted time data into a structured SunTimes object.
    - A method to set up the creatd SunTimes object with proper dates and user times.

    Single responsibility: Converts API response to SunTimes objects
    """

    @abstractmethod
    def extract_times_from_api_response(
        self, raw_api_response: requests.models.Response
    ) -> Dict[str, str]:
        """
        Extracts time-related data from the raw API response.

        Args:
            raw_api_response (requests.models.Response): The raw HTTP response from the sunrise
            -sunset API.

        Returns:
            Dict[str, str]: A dictionary containing time data as strings.

        Single Responsibility: Extract string times from the API response.
        """

    @abstractmethod
    def parse_sun_times(self, times_as_strings: Dict[str, str]) -> SunTimes:
        """
        Parses a dictionary of time strings into a SunTimes object.

        Args:
            times_as_strings (Dict[str, str]): A dictionary containing time strings as values and
            sun phases as keys

        Returns:
            SunTimes: An object representing parsed sunrise, sunset, and twilight times.

        Single Responsibility: Parsing a strings dictionary into a SunTimes object.
        """

    def handle_response(self, raw_api_response: requests.models.Response) -> SunTimes:
        """
        Handles the API response, converting it into a usable SunTimes object.

        Args:
            raw_api_response (requests.models.Response): The raw HTTP response from the API.

        Returns:
            SunTimes: A structured object containing the valid parsed sunrise, sunset, twilight
            times, and user dates and times.

        Process:
            1. Extracts raw time data using `extract_times_from_API_response`.
            2. Parses the raw data into a SunTimes object using `parse_sun_times`.

        Single Responsibility: Formatting the API response into a dictionary that can be read by
        the process_sun_times method in the SunTimes class.
        """
        string_sun_times = self.extract_times_from_api_response(raw_api_response)
        sun_times = self.parse_sun_times(string_sun_times)
        return sun_times


class ResponseHandler(AbstractResponseHandler):
    """
    Concrete implementation of AbstractResponseHandler for handling API responses.

    This class implements the methods to extract and parse time data from the API response.
    """

    def extract_times_from_api_response(
        self, raw_api_response: requests.models.Response
    ) -> Dict[str, str]:
        """
        See base class `AbstractResponseHandler` for full method documentation.
        """
        return raw_api_response.json()["results"]

    def parse_sun_times(
        self, times_as_strings: Dict[str, str]
    ) -> Dict[str, datetime.time]:
        """
        See base class `AbstractResponseHandler` for full method documentation.
        """
        return {
            "sunrise": datetime.strptime(
                times_as_strings["sunrise"], "%I:%M:%S %p"
            ).time(),
            "sunset": datetime.strptime(
                times_as_strings["sunset"], "%I:%M:%S %p"
            ).time(),
            "morning_twilight": datetime.strptime(
                times_as_strings["civil_twilight_begin"], "%I:%M:%S %p"
            ).time(),
            "night_twilight": datetime.strptime(
                times_as_strings["civil_twilight_end"], "%I:%M:%S %p"
            ).time(),
        }
