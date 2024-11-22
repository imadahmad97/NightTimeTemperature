from datetime import datetime
from app.sun_times import SunTimes
from abc import ABC, abstractmethod
import requests
from typing import Dict


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
        pass

    @abstractmethod
    def parse_sun_times(self, times_as_strings: Dict[str, str]) -> SunTimes:
        """
        Parses a dictionary of time strings into a SunTimes object.

        Args:
            times_as_strings (Dict[str, str]): A dictionary containing time strings as values and sun phases as keys

        Returns:
            SunTimes: An object representing parsed sunrise, sunset, and twilight times.

        Single Responsibility: Parsing a strings dictionary into a SunTimes object.
        """
        pass

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
            3. Sets the user's time zone for the SunTimes object.
            4. Combines the extracted times with the current date.

        Adherence to SRP:
            Partially adheres to SRP but introduces additional responsibilities:
            - Delegates data extraction and parsing to other methods (good SRP).
            - Calls methods to set user time and combine times with the date (potential SRP violation).
            These operations might belong to the `SunTimes` class or a utility method.

        Suggestion:
            Consider refactoring `set_user_time` and `combine_times_with_date` into
            a separate helper or ensuring they are encapsulated in the SunTimes class.
        """
        string_sun_times = self.extract_times_from_api_response(raw_api_response)
        sun_times = self.parse_sun_times(string_sun_times)
        sun_times.set_user_time()
        sun_times.combine_times_with_date()
        return sun_times


class ResponseHandler(AbstractResponseHandler):
    def extract_times_from_API_response(
        self, raw_api_response: requests.models.Response
    ) -> Dict[str, str]:
        return raw_api_response.json()["results"]

    def parse_sun_times(self, times_as_strings: Dict[str, str]) -> SunTimes:
        return SunTimes(
            sunrise=datetime.strptime(
                times_as_strings["sunrise"], "%I:%M:%S %p"
            ).time(),
            sunset=datetime.strptime(times_as_strings["sunset"], "%I:%M:%S %p").time(),
            morning_twilight=datetime.strptime(
                times_as_strings["civil_twilight_begin"], "%I:%M:%S %p"
            ).time(),
            night_twilight=datetime.strptime(
                times_as_strings["civil_twilight_end"], "%I:%M:%S %p"
            ).time(),
        )
