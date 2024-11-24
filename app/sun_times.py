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

from dataclasses import dataclass, field
from datetime import datetime, time, timezone
from abc import ABC, abstractmethod
from typing import Optional, Dict


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

        Returns:
            sun_times.user_time: A SunTimes class attribute containing user_time.

        Single Responsibility: Set the user time to the current UTC time.
        """

    @abstractmethod
    def combine_times_with_date(self, date):
        """
        Combines sun times with a given date, defaulting to today.

        Args:
            sun_times_dict (Dict[str, datetime.time]): A dictionary containing sun times.

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
        user_time = sun_times.set_user_time()
        sun_times.combine_times_with_date(user_time.date())
        return sun_times


@dataclass
class SunTimes(AbstractSunTimes):
    """
    A concrete implementation of AbstractSunTimes for handling and processing sun times.
    """

    sunrise: Optional[time] = None
    sunset: Optional[time] = None
    morning_twilight: Optional[time] = None
    night_twilight: Optional[time] = None
    midday_period_begins: Optional[time] = None
    midday_period_ends: Optional[time] = None
    user_time: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def set_user_time(self) -> None:
        """
        Sets the user time to the current UTC time if not already set.
        """
        self.user_time = datetime.now(timezone.utc)
        return self.user_time

    def combine_times_with_date(self, date) -> None:
        """
        Combines sun times with the current date to create full datetime objects.
        """
        self.sunrise = (
            datetime.combine(date, self.sunrise, tzinfo=timezone.utc)
            if self.sunrise
            else None
        )
        self.sunset = (
            datetime.combine(date, self.sunset, tzinfo=timezone.utc)
            if self.sunset
            else None
        )
        self.morning_twilight = (
            datetime.combine(date, self.morning_twilight, tzinfo=timezone.utc)
            if self.morning_twilight
            else None
        )
        self.night_twilight = (
            datetime.combine(date, self.night_twilight, tzinfo=timezone.utc)
            if self.night_twilight
            else None
        )
        self.midday_period_begins = (
            datetime.combine(date, self.midday_period_begins, tzinfo=timezone.utc)
            if self.midday_period_begins
            else None
        )
        self.midday_period_ends = (
            datetime.combine(date, self.midday_period_ends, tzinfo=timezone.utc)
            if self.midday_period_ends
            else None
        )

    def __repr__(self) -> str:
        """
        Provides a string representation of the sun times.

        Returns:
            str: A string representation of the sun times.
        """
        return (
            f"SunTimes(sunrise={self.sunrise}, sunset={self.sunset}, "
            f"morning_twilight={self.morning_twilight}, night_twilight={self.night_twilight}, "
            f"midday_period_begins={self.midday_period_begins}, "
            f"midday_period_ends={self.midday_period_ends}, "
            f"user_time={self.user_time})"
        )
