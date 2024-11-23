Module NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_temp
============================================================================
Module: get_temp

This module provides classes and methods for getting temperature based on user and sun times data.

Classes:
    - AbstractGetTemp: Abstract base class that defines the template for calculating temperature 
      based on user time and sun times data. Includes abstract methods for different time intervals.
    - GetTemp: Concrete implementation of `AbstractGetTemp` that provides specific methods for 
      calculating temperature based on user time and sun times data.

Usage:
    The `AbstractGetTemp` class should be subclassed to create custom temperature calculators that 
    implement the `user_in_midday_period`, `user_in_night_period`, `user_in_morning_twilight`, and 
    `user_in_night_twilight` methods. The `GetTemp` class provides one such implementation for 
    handling typical temperature calculations based on user time and sun times data.

Dependencies:
    - flask: Used for accessing the current Flask application configuration.
    - abc: Provides the abstract base class functionality.

Classes
-------

`AbstractGetTemp()`
:   An abstract base class that defines the interface for temperature calculators.
    
    This class provides abstract methods for calculating temperature based on user time and sun
    times data. Subclasses must implement these methods to provide specific temperature calculation
    logic.
    
    Single responsibility: Define the interface for temperature calculators.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_temp.GetTemp

    ### Static methods

    `user_in_midday_period() ‑> int`
    :   Calculates the temperature during the midday period.
        
        Returns:
            int: The calculated temperature during the midday period.
        
        Single Responsibility: Calculate the temperature during the midday period.

    `user_in_morning_twilight(morning_prop: float) ‑> int`
    :   Calculates the temperature during the morning twilight period based on sun times data.
        
        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.
        
        Returns:
            int: The calculated temperature during the morning twilight period.
        
        Single Responsibility: Calculate the temperature during the morning twilight period.

    `user_in_night_period() ‑> int`
    :   Calculates the temperature during the night period.
        
        Returns:
            int: The calculated temperature during the night period.
        
        Single Responsibility: Calculate the temperature during the night period.

    `user_in_night_twilight(night_prop: float) ‑> int`
    :   Calculates the temperature during the night twilight period based on sun times data.
        
        Args:
            sun_times (SunTimes): A structured object containing processed sun times data.
        
        Returns:
            int: The calculated temperature during the night twilight period.
        
        Single Responsibility: Calculate the temperature during the night twilight period.

`GetTemp()`
:   Concrete implementation of AbstractGetTemp for calculating temperature based on user time and
    sun times data.
    
    This class implements the methods to calculate temperature during different time intervals
    based on user time and sun times data.
    
    Single responsibility: Calculate temperature based on user time and sun times data.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.calculate_temp.calculate_temp_utils.get_temp.AbstractGetTemp
    * abc.ABC

    ### Static methods

    `user_in_midday_period() ‑> int`
    :   See base class `AbstractGetTemp` for full method documentation.

    `user_in_morning_twilight(morning_prop: float) ‑> int`
    :   See base class `AbstractGetTemp` for full method documentation.

    `user_in_night_period() ‑> int`
    :   See base class `AbstractGetTemp` for full method documentation.

    `user_in_night_twilight(night_prop: float) ‑> int`
    :   See base class `AbstractGetTemp` for full method documentation.