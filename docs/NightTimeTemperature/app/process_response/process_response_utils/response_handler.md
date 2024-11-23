Module NightTimeTemperature.app.process_response.process_response_utils.response_handler
========================================================================================
Module: response_handler

This module provides classes and methods for handling API responses from the sunrise-sunset API.

Classes:
    - AbstractResponseHandler: An abstract base class that defines the template for converting API 
      responses into `SunTimes` objects. It includes abstract methods for extracting and parsing 
      time data from the API response.
    - ResponseHandler: A concrete implementation of `AbstractResponseHandler` that provides specific
      methods for extracting and parsing time data from the API response.

Usage:
    The `AbstractResponseHandler` class should be subclassed to create custom response handlers that
    implement the `extract_times_from_api_response` and `parse_sun_times` methods. The 
    `ResponseHandler` class provides one such implementation for handling typical sunrise and sunset
    API responses.

Dependencies:
    - abc: Provides the abstract base class functionality.
    - datetime: Used for parsing and handling date and time data.
    - typing: Provides type hinting for better code readability and maintenance.
    - requests: Used for handling HTTP requests and responses.
    - app.sun_times: Contains the `SunTimes` class used to structure the parsed time data.

Classes
-------

`AbstractResponseHandler()`
:   Abstract base class for converting API responses into SunTime Objects.
    
    This class provides a template for response handlers by defining:
    - A method to extract raw time data from the API response.
    - A method to parse the extracted time data into a structured SunTimes object.
    - A method to set up the creatd SunTimes object with proper dates and user times.
    
    Single responsibility: Converts API response to SunTimes objects

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * NightTimeTemperature.app.process_response.process_response_utils.response_handler.ResponseHandler

    ### Methods

    `extract_times_from_api_response(self, raw_api_response: requests.models.Response) ‑> Dict[str, str]`
    :   Extracts time-related data from the raw API response.
        
        Args:
            raw_api_response (requests.models.Response): The raw HTTP response from the sunrise
            -sunset API.
        
        Returns:
            Dict[str, str]: A dictionary containing time data as strings.
        
        Single Responsibility: Extract string times from the API response.

    `handle_response(self, raw_api_response: requests.models.Response) ‑> app.sun_times.SunTimes`
    :   Handles the API response, converting it into a usable SunTimes object.
        
        Args:
            raw_api_response (requests.models.Response): The raw HTTP response from the API.
        
        Returns:
            SunTimes: A structured object containing the valid parsed sunrise, sunset, twilight
            times, and user dates and times.
        
        Process:
            1. Extracts raw time data using `extract_times_from_API_response`.
            2. Parses the raw data into a SunTimes object using `parse_sun_times`.
        
        Single Responsibility: Formatting the API response into a dictionary that can be read by
        the process_sun_times method in the SunTimes class.

    `parse_sun_times(self, times_as_strings: Dict[str, str]) ‑> app.sun_times.SunTimes`
    :   Parses a dictionary of time strings into a SunTimes object.
        
        Args:
            times_as_strings (Dict[str, str]): A dictionary containing time strings as values and
            sun phases as keys
        
        Returns:
            SunTimes: An object representing parsed sunrise, sunset, and twilight times.
        
        Single Responsibility: Parsing a strings dictionary into a SunTimes object.

`ResponseHandler()`
:   Concrete implementation of AbstractResponseHandler for handling API responses.
    
    This class implements the methods to extract and parse time data from the API response.

    ### Ancestors (in MRO)

    * NightTimeTemperature.app.process_response.process_response_utils.response_handler.AbstractResponseHandler
    * abc.ABC

    ### Methods

    `extract_times_from_api_response(self, raw_api_response: requests.models.Response) ‑> Dict[str, str]`
    :   See base class `AbstractResponseHandler` for full method documentation.

    `parse_sun_times(self, times_as_strings: Dict[str, str]) ‑> Dict[str, <method 'time' of 'datetime.datetime' objects>]`
    :   See base class `AbstractResponseHandler` for full method documentation.