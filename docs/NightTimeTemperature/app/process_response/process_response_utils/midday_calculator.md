Module NightTimeTemperature.app.process_response.process_response_utils.midday_calculator
=========================================================================================
Module: midday_calculator

This module provides classes and methods for processing midday periods based on SunTimes.

Classes:
    - AbstractMiddayPeriodCalculator: An abstract base class that defines the template for 
      calculating 
      and adjusting midday periods. It includes abstract methods for calculating the midday period 
      and adjusting it to ensure logical consistency.
    - MiddayPeriodCalculator: A concrete implementation of `AbstractMiddayPeriodCalculator` that 
      provides specific methods for calculating and adjusting midday periods based on SunTimes.

Usage:
    The `AbstractMiddayPeriodCalculator` class should be subclassed to create custom midday period 
    calculators that implement the `calculate_midday_period` and `midday_period_adjustment` methods. 
    The `MiddayPeriodCalculator` class provides one such implementation for handling typical 
    calculations and adjustments of midday periods.

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for handling date and time calculations.
    - app.sun_times: Contains the `SunTimes` class used to structure the midday period data.

Classes
-------

`AbstractMiddayPeriodCalculator()`
:   Abstract base class for calculating and adjusting midday periods based on SunTimes.
    
    This class provides a template for midday period calculators by defining:
    - A method to calculate the midday period based on sunrise and sunset times.
    - A method to adjust the calculated midday period to ensure logical consistency.
    - A method to handle the overall process of calculating and adjusting midday periods.
    
    Single responsibility: Calculates and adjusts midday periods.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.process_response.process_response_utils.midday_calculator.MiddayPeriodCalculator

    ### Methods

    `calculate_midday_period(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Calculates the midday period based on sunrise and sunset times.
        
        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.
        
        Returns:
            SunTimes: An object with calculated midday period times.
        
        Single Responsibility: Calculate midday period times from sun times.

    `midday_period_adjustment(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Adjusts the calculated midday period to ensure logical consistency.
        
        Args:
            sun_times (SunTimes): An object containing calculated midday period times.
        
        Returns:
            SunTimes: An object with adjusted midday period times.
        
        Single Responsibility: Adjust midday period times to ensure they are logically consistent.

    `process_midday_period(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   Handles the process of calculating and adjusting midday periods.
        
        Args:
            sun_times (SunTimes): An object containing sunrise, sunset, and twilight times.
        
        Returns:
            SunTimes: An object with calculated and adjusted midday period times.
        
        Process:
            1. Calculates midday period using `calculate_midday_period`.
            2. Adjusts the calculated midday period using `midday_period_adjustment`.
        
        Single Responsibility: Manage the overall process of processing midday periods.

`MiddayPeriodCalculator()`
:   Concrete implementation of AbstractMiddayPeriodCalculator for calculating and adjusting midday
    periods.
    
    This class implements the methods to calculate and adjust midday periods based on SunTimes.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.process_response.process_response_utils.midday_calculator.AbstractMiddayPeriodCalculator
    * abc.ABC

    ### Methods

    `calculate_midday_period(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   See base class `AbstractMiddayPeriodCalculator` for full method documentation.

    `midday_period_adjustment(self, sun_times: app.sun_times.SunTimes) ‑> app.sun_times.SunTimes`
    :   See base class `AbstractMiddayPeriodCalculator` for full method documentation.