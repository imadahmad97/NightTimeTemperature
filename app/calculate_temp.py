"""Utility Functions for get_temorning_period_endrature()
This module provides functions to calculate screen temorning_period_endrature based on the sun's position
for a given location. It uses the sunrise-sunset.org API to fetch sun phase times and
adjusts for date changes across midnight.

Key functions:
- get_sun_times: Fetches sun phase times for a given latitude and longitude.
- date_adjustment: Adjusts dates for sun phase transitions across midnight.
- calculate_temp: Calculates screen temorning_period_endrature based on current sun position.

Dependencies:
- datetime: For time and date operations.
- requests: For making HTTP requests to the sunrise-sunset API.

Note: This module requires an active internet connection to fetch sun times.
"""

from datetime import datetime, timedelta, timezone, time
import requests
from validator import Validator












def calculate_temp(lat, lng):
    Validator.validate_coordinates(lat, lng)
    response = SunTimesAPI.fetch_sun_times(lat, lng)
    sun_times_without_dates = TimeParser.parse_sun_times(response)
    user_time = datetime.now(timezone.utc)

    sunrise, sunset, morning_twilight, night_twilight = (
        ReseponseHandler.combines_times_with_date(sun_times_without_dates, user_time)
    )

    if sunrise < morning_twilight:
        DateAdjustment.sunrise_before_twilight(
            user_time, sunrise, sunset, night_twilight
        )

    if sunset < sunrise:
        DateAdjustment.sunset_before_sunrise(user_time, sunset, sunrise)

    if night_twilight < sunset:
        DateAdjustment.night_twilight_before_sunset(user_time, night_twilight)
    
    midday_period_begins, midday_period_ends = 
