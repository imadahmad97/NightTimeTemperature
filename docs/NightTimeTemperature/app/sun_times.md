Module NightTimeTemperature.app.sun_times
=========================================
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

Classes
-------

`AbstractSunTimes()`
:   Abstract base class for handling and processing sun times.
    
    This class defines the template for methods that:
    - Set the user time.
    - Combine sun times with a specific date.
    - Process a dictionary of sun times into a SunTimes object.
    
    Single Responsibility: Provides the framework for processing and representing sun times.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.sun_times.SunTimes

    ### Static methods

    `process_sun_times(sun_times_dict: Dict[str, <method 'time' of 'datetime.datetime' objects>]) ‑> NightTimeTemperature.app.sun_times.SunTimes`
    :   Processes a dictionary of sun times into a SunTimes object.
        
        Args:
            sun_times_dict (Dict[str, datetime.time]): A dictionary containing sun times.
        
        Returns:
            SunTimes: An object representing the processed sun times.
        
        Single Responsibility: Convert a dictionary of sun times into a SunTimes object.

    ### Methods

    `combine_times_with_date(self)`
    :   Combines sun times with a given date, defaulting to today.
        
        Single Responsibility: Combine sun times with today's date.

    `set_user_time(self)`
    :   Sets the user time, defaulting to the current UTC time.
        
        Single Responsibility: Set the user time to the current UTC time.

`SunTimes(sunrise: Optional[datetime.time] = None, sunset: Optional[datetime.time] = None, morning_twilight: Optional[datetime.time] = None, night_twilight: Optional[datetime.time] = None, midday_period_begins: Optional[datetime.time] = None, midday_period_ends: Optional[datetime.time] = None, user_time: Optional[datetime.datetime] = <factory>)`
:   A concrete implementation of AbstractSunTimes for handling and processing sun times.
    
    Attributes:
        sunrise (Optional[time]): Time of sunrise.
        sunset (Optional[time]): Time of sunset.
        morning_twilight (Optional[time]): Time of morning twilight.
        night_twilight (Optional[time]): Time of night twilight.
        midday_period_begins (Optional[time]): Time when the midday period begins.
        midday_period_ends (Optional[time]): Time when the midday period ends.
        user_time (Optional[datetime]): User-defined time or current UTC time by default.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.sun_times.AbstractSunTimes
    * abc.ABC

    ### Class variables

    `midday_period_begins: Optional[datetime.time]`
    :

    `midday_period_ends: Optional[datetime.time]`
    :

    `morning_twilight: Optional[datetime.time]`
    :

    `night_twilight: Optional[datetime.time]`
    :

    `sunrise: Optional[datetime.time]`
    :

    `sunset: Optional[datetime.time]`
    :

    `user_time: Optional[datetime.datetime]`
    :

    ### Methods

    `combine_times_with_date(self) ‑> None`
    :   Combines sun times with the current date to create full datetime objects.

    `set_user_time(self) ‑> None`
    :   Sets the user time to the current UTC time if not already set.