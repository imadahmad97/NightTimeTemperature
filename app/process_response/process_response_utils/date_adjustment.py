"""
Module: date_adjustment

This module provides classes and methods for adjusting dates based on SunTimes.

Classes:
    - AbstractDateAdjustment: An abstract base class that defines the template for adjusting dates 
      based on sunrise, sunset, and twilight times. It includes abstract methods for handling 
      specific date adjustment scenarios.
    - DateAdjustment: A concrete implementation of `AbstractDateAdjustment` that provides specific 
      methods for adjusting dates based on SunTimes.

Usage:
    The `AbstractDateAdjustment` class should be subclassed to create custom date adjustment
    handlers that implement the `sunrise_before_twilight`, `sunset_before_sunrise`, and 
    `night_twilight_before_sunset` methods. The `DateAdjustment` class provides one such
    implementation for handling typical date adjustments.

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for handling date and time calculations.
    - app.sun_times: Contains the `SunTimes` class used to structure the date-adjusted time data.
"""

from datetime import time, timedelta
from abc import ABC, abstractmethod
from app.sun_times import SunTimes


class AbstractDateAdjustment(ABC):
    """
    Abstract base class for adjusting dates based on SunTimes.

    This class provides a template for date adjustment handlers by defining:
    - A method to adjust dates when sunrise occurs before morning twilight.
    - A method to adjust dates when sunset occurs before sunrise.
    - A method to adjust dates when night twilight occurs before sunset.
    - A method to handle the overall process of adjusting dates.

    Single responsibility: Adjusts dates based on sunrise, sunset, and twilight times.
    """

    @abstractmethod
    def sunrise_before_twilight(self, sun_times: SunTimes) -> SunTimes:
        """
        Adjusts dates when sunrise occurs before morning twilight.

        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.

        Returns:
            SunTimes: An object with adjusted sunrise, sunset, and twilight times.

        Single Responsibility: Adjust dates when sunrise is before morning twilight.
        """

    @abstractmethod
    def sunset_before_sunrise(self, sun_times: SunTimes) -> SunTimes:
        """
        Adjusts dates when sunset occurs before sunrise.

        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.

        Returns:
            SunTimes: An object with adjusted sunset and twilight times.

        Single Responsibility: Adjust dates when sunset is before sunrise.
        """

    @abstractmethod
    def night_twilight_before_sunset(self, sun_times: SunTimes) -> SunTimes:
        """
        Adjusts dates when night twilight occurs before sunset.

        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.

        Returns:
            SunTimes: An object with adjusted night twilight times.

        Single Responsibility: Adjust dates when night twilight is before sunset.
        """

    def adjust_dates(self, sun_times: SunTimes) -> SunTimes:
        """
        Handles the process of adjusting dates based on sunrise, sunset, and twilight times.

        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.

        Returns:
            SunTimes: An object with adjusted sunrise, sunset, and twilight times.

        Process:
            1. Adjusts dates if sunrise occurs before morning twilight using
            `sunrise_before_twilight`.
            2. Adjusts dates if sunset occurs before sunrise using `sunset_before_sunrise`.
            3. Adjusts dates if night twilight occurs before sunset using
            `night_twilight_before_sunset`.

        Single Responsibility: Manage the overall process of adjusting dates based on sun times.
        """
        if sun_times.sunrise < sun_times.morning_twilight:
            sun_times = self.sunrise_before_twilight(sun_times)

        if sun_times.sunset < sun_times.sunrise:
            sun_times = self.sunset_before_sunrise(sun_times)

        if sun_times.night_twilight < sun_times.sunset:
            sun_times = self.night_twilight_before_sunset(sun_times)

        return sun_times


class DateAdjustment(AbstractDateAdjustment):
    """
    Concrete implementation of AbstractDateAdjustment for adjusting dates based on SunTimes.

    This class implements the methods to adjust dates based on specific scenarios involving sunrise,
    sunset, and twilight times.
    """

    def sunrise_before_twilight(self, sun_times: SunTimes) -> SunTimes:
        """
        See base class `AbstractDateAdjustment` for full method documentation.
        """
        if time(00, 00) <= sun_times.user_time.time() < sun_times.sunrise.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunrise += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    def sunset_before_sunrise(self, sun_times: SunTimes) -> SunTimes:
        """
        See base class `AbstractDateAdjustment` for full method documentation.
        """
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    def night_twilight_before_sunset(self, sun_times: SunTimes) -> SunTimes:
        """
        See base class `AbstractDateAdjustment` for full method documentation.
        """
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times
