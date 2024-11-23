Module NightTimeTemperature.app.process_response.process_response
=================================================================
Module: process_api_call

This module provides a class for processing API calls to fetch and process sun times data.

Classes:
    - ProcessAPICall: A class that handles the process of fetching sun times data from an API, 
      formatting it, adjusting dates, and calculating midday periods.

Usage:
    The `ProcessAPICall` class provides a static method to process API calls and return a structured 
    `SunTimes` object containing the processed sun times data.

Dependencies:
    - app.sun_times: Contains `SunTimes` class used to structure the parsed and processed time data.
    - .process_response_utils.response_handler: Contains the `ResponseHandler` class for handling 
       API responses.
    - .process_response_utils.midday_calculator: Contains the `MiddayPeriodCalculator` class for 
       calculating midday periods.
    - .process_response_utils.date_adjustment: Contains `DateAdjustment` class for adjusting dates.
    - .process_response_utils.sun_times_api: Contains the `SunTimesAPI` class for fetching sun times
       data from an API.

Classes
-------

`ProcessAPICall()`
:   A class that handles the process of fetching sun times data from an API, validating it,
    and processing it into a SunTimes object.
    
    This class provides methods to instantiate necessary components and process API calls
    to return a structured `SunTimes` object containing the processed sun times data.
    
    Single responsibility: Process API calls to fetch and process sun times data.
    
    Initializes the necessary components for processing API calls.

    ### Methods

    `process_api_call(self, response) ‑> app.sun_times.SunTimes`
    :   Processes an API call to fetch and process sun times data.
        
        Args:
            response (dict): The API response containing sun times data.
        
        Returns:
            SunTimes: A structured object containing the processed sun times data.
        
        Process:
            1. Handles the API response using `ResponseHandler`.
            2. Processes the raw sun times data using `SunTimes`.
            3. Adjusts the dates using `DateAdjustment`.
            4. Calculates the midday period using `MiddayPeriodCalculator`.
        
        Single Responsibility: Manage the entire process of fetching and processing sun times data.

    `validate_response(self, response) ‑> bool`
    :   Validates the API response to ensure it contains the expected data.
        
        Args:
            response (dict): The API response containing sun times data.
        
        Returns:
            bool: True if the response is valid, False otherwise.
        
        Single Responsibility: Validate the API response format and content.