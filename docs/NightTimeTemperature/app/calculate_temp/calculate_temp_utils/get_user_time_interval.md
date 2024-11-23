Module NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_user_time_interval
==========================================================================================
Module: get_user_time_interval

This module provides classes and methods for calculating time intervals based on sun times data.

Classes:
    - AbstractTimeIntervalCalculator: Abstract base class that defines the template for calculating 
      time intervals based on sun times data. It includes abstract methods for instantiating
      proportions and getting intervals.
    - TimeIntervalCalculator: Concrete implementation of `AbstractTimeIntervalCalculator` that
      provides specific methods for calculating time intervals based on sun times data.

Usage:
    The `AbstractTimeIntervalCalculator` class should be subclassed to create custom interval 
    calculators that implement the `instantiate_proportion` and `get_interval` methods. The 
    `TimeIntervalCalculator` class provides one such implementation for handling typical
    calculations based on sun times data.

Dependencies:
    - abc: Provides the abstract base class functionality.
    - app.sun_times: Contains the `SunTimes` class used to structure the parsed time data.
    - .proportion_calculator: Gives `ProportionCalculator` class for calculating user proportions.
    - .get_temp: Provides the `GetTemp` class for temperature calculations based on time intervals.

Classes
-------

`AbstractTimeIntervalCalculator()`
:   An abstract base class that defines the interface for time interval calculators.
    
    This class provides abstract methods for calculating time intervals based on sun times data.
    Subclasses must implement these methods to provide specific interval calculation logic.
    
    Single responsibility: Define the interface for time interval calculators.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_user_time_interval.TimeIntervalCalculator

    ### Static methods

    `instantiate_proportion(sun_times: app.sun_times.SunTimes) ‑> float`
    :   Instantiates the proportion calculator to get user proportions for morning/night intervals.
        
        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.
        
        Returns:
            float: The calculated user proportions for morning and night intervals.
        
        Single Responsibility: Instantiate the proportion calculator to get user proportions.

    ### Methods

    `get_interval(self, sun_times: app.sun_times.SunTimes) ‑> int`
    :   Calculates the time interval based on user time and sun times data.
        
        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.
        
        Returns:
            int: The calculated time interval.
        
        Single Responsibility: Calculate the time interval based on user time and sun times data.

`TimeIntervalCalculator()`
:   Concrete implementation of AbstractTimeIntervalCalculator for calculating time intervals based
    on sun times data.
    
    This class implements the methods to instantiate the proportion calculator and calculate time
    intervals based on user time and sun times data.
    
    Single responsibility: Calculate time intervals based on user time and sun times data.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_user_time_interval.AbstractTimeIntervalCalculator
    * abc.ABC

    ### Static methods

    `instantiate_proportion(sun_times: app.sun_times.SunTimes) ‑> float`
    :   See base class `AbstractTimeIntervalCalculator` for full method documentation.

    ### Methods

    `get_interval(self, sun_times: app.sun_times.SunTimes) ‑> int`
    :   See base class `AbstractTimeIntervalCalculator` for full method documentation.