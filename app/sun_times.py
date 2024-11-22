"""
Module: sun_times

This module provides classes and methods for handling and processing sun times.

Classes:
    - AbstractSunTimes: An abstract base class that defines the template for handling and processing
      sun times. It includes abstract methods for setting user time, combining sun times with a 
      specific date, and providing a string representation of the sun times.
    - SunTimes: A concrete implementation of `AbstractSunTimes` that provides specific methods for
      setting user time, combining sun times with a specific date, and representing sun times as a 
      string.

Usage:
    The `AbstractSunTimes` class should be subclassed to create custom sun time handlers that 
    implement the `set_user_time`, `combine_times_with_date`, and `__repr__` methods. The `SunTimes`
    class provides one such implementation for handling typical sun times.

Example:
    sun_times_dict = {
        "sunrise": datetime.time(6, 0),
        "sunset": datetime.time(18, 0),
        "morning_twilight": datetime.time(5, 30),
        "night_twilight": datetime.time(18, 30),
    }
    sun_times = AbstractSunTimes.process_sun_times(sun_times_dict)
    print(sun_times)

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for parsing and handling date and time data.
    - typing: Provides type hinting for better code readability and maintenance.
"""

from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict


class AbstractSunTimes(ABC):
    """
    Abstract base class for handling and processing sun times.

    This class defines the template for methods that:
    - Set the user time.
    - Combine sun times with a specific date.
    - Process a dictionary of sun times into a SunTimes object.

    Single Responsibility: Provides the framework for processing and representing sun times.
    """

    @abstractmethod
    def set_user_time(self):
        """
        Sets the user time, defaulting to the current UTC time.

        Single Responsibility: Set the user time to the current UTC time.
        """

    @abstractmethod
    def combine_times_with_date(self):
        """
        Combines sun times with a given date, defaulting to today.

        Single Responsibility: Combine sun times with today's date.
        """

    @abstractmethod
    def __repr__(self):
        """
        Provides a string representation of the sun times.

        Single Responsibility: Represent the sun times as a string.
        """

    @staticmethod
    def process_sun_times(sun_times_dict: Dict[str, datetime.time]) -> "SunTimes":
        """
        Processes a dictionary of sun times into a SunTimes object.

        Args:
            sun_times_dict (Dict[str, datetime.time]): A dictionary containing sun times.

        Returns:
            SunTimes: An object representing the processed sun times.

        Single Responsibility: Convert a dictionary of sun times into a SunTimes object.
        """
        sun_times = SunTimes(
            sunrise=sun_times_dict.get("sunrise"),
            sunset=sun_times_dict.get("sunset"),
            morning_twilight=sun_times_dict.get("morning_twilight"),
            night_twilight=sun_times_dict.get("night_twilight"),
        )
        sun_times.set_user_time()
        sun_times.combine_times_with_date()
        return sun_times


class SunTimes(AbstractSunTimes):
    """
    Concrete implementation of AbstractSunTimes for handling and processing sun times.

    This class provides methods to:
    - Set the user time.
    - Combine sun times with a specific date.
    - Represent sun times as a string.
    """

    def __init__(
        self,
        sunrise=None,
        sunset=None,
        morning_twilight=None,
        night_twilight=None,
        midday_period_begins=None,
        midday_period_ends=None,
        user_time=None,
    ):
        """
        Initializes the SunTimes object with optional sun times and user time.

        Args:
            sunrise (datetime.time, optional): Time of sunrise.
            sunset (datetime.time, optional): Time of sunset.
            morning_twilight (datetime.time, optional): Time of morning twilight.
            night_twilight (datetime.time, optional): Time of night twilight.
            midday_period_begins (datetime.time, optional): Time when midday period begins.
            midday_period_ends (datetime.time, optional): Time when midday period ends.
            user_time (datetime, optional): User-defined time.

        Single Responsibility: Initialize the SunTimes object with provided sun times and user time.
        """
        self.sunrise = sunrise
        self.sunset = sunset
        self.morning_twilight = morning_twilight
        self.night_twilight = night_twilight
        self.midday_period_begins = midday_period_begins
        self.midday_period_ends = midday_period_ends
        self.user_time = user_time

    def set_user_time(self) -> None:
        """
        See base class 'AbstractSunTimes' for full method documentation.
        """
        self.user_time = datetime.now(timezone.utc)

    def combine_times_with_date(self) -> None:
        """
        See base class 'AbstractSunTimes' for full method documentation.
        """
        self.set_user_time()

        date = self.user_time.date()

        self.sunrise = datetime.combine(date, self.sunrise, tzinfo=timezone.utc)
        self.sunset = datetime.combine(date, self.sunset, tzinfo=timezone.utc)
        self.morning_twilight = datetime.combine(
            date, self.morning_twilight, tzinfo=timezone.utc
        )
        self.night_twilight = datetime.combine(
            date, self.night_twilight, tzinfo=timezone.utc
        )

    def __repr__(self) -> str:
        """
        Provides a string representation of the sun times.

        Returns:
            str: A string representation of the sun times.

        Single Responsibility: Represent the sun times as a string.
        """
        return (
            f"SunTimes(sunrise={self.sunrise}, sunset={self.sunset}, "
            f"morning_twilight={self.morning_twilight}, night_twilight={self.night_twilight}, "
            f"midday_period_begins={self.midday_period_begins}, "
            f"midday_period_ends={self.midday_period_ends}, "
            f"user_time={self.user_time})"
        )
