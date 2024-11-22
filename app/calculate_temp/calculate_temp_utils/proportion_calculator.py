"""
Module: proportion_calculator

This module provides classes and methods for calculating user proportions based on sun times data.

Classes:
    - AbstractPropoprtionCalculator: Abstract base class that defines the template for calculating 
      user proportions within given intervals. It includes abstract methods for calculating user 
      proportions for morning and night intervals based on sun times data.
    - ProportionCalculator: Concrete implementation of `AbstractPropoprtionCalculator` that provides 
      specific methods for calculating user proportions for morning and night intervals.

Usage:
    The `AbstractPropoprtionCalculator` class should be subclassed to create custom proportion 
    calculators that implement the `calculate_user_proportion`, `get_user_prop_morning`, and 
    `get_user_prop_night` methods. The `ProportionCalculator` class provides one such implementation
    for handling typical calculations based on sun times data.

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for parsing and handling date and time data.
    - typing: Provides type hinting for better code readability and maintenance.
    - app.sun_times: Contains the `SunTimes` class used to structure the parsed time data.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from app.sun_times import SunTimes


class AbstractPropoprtionCalculator(ABC):
    """
    An abstract base class that defines the interface for proportion calculators.

    This class provides abstract methods for calculating user proportions based on sun times data.
    Subclasses must implement these methods to provide specific proportion calculation logic.

    Single responsibility: Define the interface for proportion calculators.
    """

    @staticmethod
    @abstractmethod
    def calculate_user_proportion(
        user_time: datetime, start_time: datetime, interval_length: timedelta
    ) -> float:
        """
        Calculates the user proportion within a given interval.

        Args:
            user_time (datetime): The user's time.
            start_time (datetime): The start time of the interval.
            interval_length (timedelta): The length of the interval.

        Returns:
            float: The calculated user proportion.

        Single Responsibility: Calculate the user proportion within a given interval.
        """

    @abstractmethod
    def get_user_prop_morning(self, sun_times: SunTimes) -> float:
        """
        Calculates the user proportion for the morning interval based on sun times data.

        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.

        Returns:
            float: The calculated user proportion for the morning interval.

        Single Responsibility: Calculate the user proportion for the morning interval.
        """

    @abstractmethod
    def get_user_prop_night(self, sun_times: SunTimes) -> float:
        """
        Calculates the user proportion for the night interval based on sun times data.

        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.

        Returns:
            float: The calculated user proportion for the night interval.

        Single Responsibility: Calculate the user proportion for the night interval.
        """


class ProportionCalculator(AbstractPropoprtionCalculator):
    """
    Concrete implementation of AbstractPropoprtionCalculator for calculating user proportions for
    morning and night intervals.

    This class implements the methods to calculate the user proportion within a given interval,
    as well as specific methods to calculate user proportions for morning and night intervals
    based on sun times data.

    Single responsibility: Calculate user proportions for morning and night intervals using sun
    times data.
    """

    @staticmethod
    def calculate_user_proportion(
        user_time: datetime, start_time: datetime, interval_length: timedelta
    ) -> float:
        """
        See base class `AbstractProportionCalculator` for full method documentation.
        """
        return (user_time - start_time) / (2 * interval_length)

    def get_user_prop_morning(self, sun_times: SunTimes) -> float:
        """
        See base class `AbstractProportionCalculator` for full method documentation.
        """
        morning_twilight_length = sun_times.sunrise - sun_times.morning_twilight
        return self.calculate_user_proportion(
            sun_times.user_time,
            sun_times.morning_twilight,
            morning_twilight_length,
        )

    def get_user_prop_night(self, sun_times: SunTimes) -> float:
        """
        See base class `AbstractProportionCalculator` for full method documentation.
        """
        night_twilight_length = sun_times.night_twilight - sun_times.sunset
        return self.calculate_user_proportion(
            sun_times.user_time,
            sun_times.midday_period_ends,
            night_twilight_length,
        )
