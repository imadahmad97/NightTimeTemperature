"""
This module provides functionality to calculate temperature based on sun times data
Classes:
    - CalculateTemp: A class that provides methods to verify and calculate temperature from sun_time
    data
"""

from typing import List
from app.sun_times import SunTimes
from .calculate_temp_utils.get_user_time_interval import TimeIntervalCalculator


class CalculateTemp:
    """
    A class that provides methods to calculate the temperature based on sun times data
    and verify the completeness of SunTimes objects.

    This class is responsible for utilizing the `GetTemp` utility to calculate the temperature
    from a structured `SunTimes` object and verifying the presence of all required attributes
    in a SunTimes object.

    Single responsibility: Calculate temperature using sun times data and verify SunTimes objects.
    """

    @staticmethod
    def calculate_temp(sun_times: SunTimes) -> int:
        """
        Calculates the temperature based on sun times data.

        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.

        Returns:
            int: The calculated temperature.

        Single Responsibility: Use the `GetTemp` utility to calculate the temperature from sun times
        data.
        """
        temp_calculator: TimeIntervalCalculator = TimeIntervalCalculator()
        return temp_calculator.get_interval(sun_times)

    @staticmethod
    def verify_sun_times(sun_times: SunTimes) -> bool:
        """
        Verifies if all required attributes are present in the SunTimes object.

        Args:
            sun_times (SunTimes): A SunTimes object to be verified.

        Returns:
            bool: True if all required attributes are present, False otherwise.

        Single Responsibility: Verify the completeness of a SunTimes object.
        """
        required_attributes: List[str] = [
            "sunrise",
            "sunset",
            "morning_twilight",
            "night_twilight",
            "midday_period_begins",
            "midday_period_ends",
            "user_time",
        ]

        for attr in required_attributes:
            if not hasattr(sun_times, attr):
                return False
        return True
