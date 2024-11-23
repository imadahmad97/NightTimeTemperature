Module NightTimeTemperature.app.main
====================================
Module: main

This module provides the main function for fetching sun times data, processing the API response, 
and calculating the temperature based on the processed data.

Functions:
    - main: Fetches sun times data based on latitude and longitude, processes the API response, 
      and calculates the temperature.

Dependencies:
    - flask: Used for creating JSON responses.
    - .process_response.process_response: Contains the `ProcessAPICall` class for processing API 
       responses.
    - .process_response.process_response_utils.sun_times_api: Contains the `SunTimesAPI` class for 
       fetching sun times data.
    - .calculate_temp.calculate_temp: Contains the `CalculateTemp` class for calculating temperature
       based on processed sun times data.

Functions
---------

`main(lat: float, lng: float) ‑> flask.wrappers.Response`
:   Fetches sun times data based on latitude and longitude, processes the API response,
    and calculates the temperature.
    
    Args:
        lat (float): The latitude for the API call.
        lng (float): The longitude for the API call.
    
    Returns:
        Response: A JSON response containing the calculated temperature.
    
    Process:
        1. Fetches sun times data using `SunTimesAPI`.
        2. Processes the API response using `ProcessAPICall`.
        3. Calculates the temperature using `CalculateTemp`.
    
    Single Responsibility: Manage the entire process of fetching, processing sun times data, and
    calculating temperature.