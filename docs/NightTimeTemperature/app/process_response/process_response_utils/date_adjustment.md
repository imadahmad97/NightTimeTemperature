Module NightTimeTemperature.app.process_response.process_response_utils.date_adjustment
=======================================================================================
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

Classes
-------

`AbstractDateAdjustment()`
:   Abstract base class for adjusting dates based on SunTimes.
    
    This class provides a template for date adjustment handlers by defining:
    - A method to adjust dates when sunrise occurs before morning twilight.
    - A method to adjust dates when sunset occurs before sunrise.
    - A method to adjust dates when night twilight occurs before sunset.
    - A method to handle the overall process of adjusting dates.
    
    Single responsibility: Adjusts dates based on sunrise, sunset, and twilight times.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.process_response.process_response_utils.date_adjustment.DateAdjustment

    ### Methods

    `adjust_dates(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Handles the process of adjusting dates based on sunrise, sunset, and twilight times.
        
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

    `night_twilight_before_sunset(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Adjusts dates when night twilight occurs before sunset.
        
        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.
        
        Returns:
            SunTimes: An object with adjusted night twilight times.
        
        Single Responsibility: Adjust dates when night twilight is before sunset.

    `sunrise_before_twilight(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Adjusts dates when sunrise occurs before morning twilight.
        
        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.
        
        Returns:
            SunTimes: An object with adjusted sunrise, sunset, and twilight times.
        
        Single Responsibility: Adjust dates when sunrise is before morning twilight.

    `sunset_before_sunrise(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Adjusts dates when sunset occurs before sunrise.
        
        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.
        
        Returns:
            SunTimes: An object with adjusted sunset and twilight times.
        
        Single Responsibility: Adjust dates when sunset is before sunrise.

`DateAdjustment()`
:   Concrete implementation of AbstractDateAdjustment for adjusting dates based on SunTimes.
    
    This class implements the methods to adjust dates based on specific scenarios involving sunrise,
    sunset, and twilight times.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.process_response.process_response_utils.date_adjustment.AbstractDateAdjustment
    * abc.ABC

    ### Methods

    `night_twilight_before_sunset(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   See base class `AbstractDateAdjustment` for full method documentation.

    `sunrise_before_twilight(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   See base class `AbstractDateAdjustment` for full method documentation.

    `sunset_before_sunrise(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   See base class `AbstractDateAdjustment` for full method documentation.