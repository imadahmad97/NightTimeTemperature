"""Utility Functions for get_temperature()
This module provides functions to calculate screen temperature based on the sun's position
for a given location. It uses the sunrise-sunset.org API to fetch sun phase times and
adjusts for date changes across midnight.

Key functions:
- get_sun_times: Fetches sun phase times for a given latitude and longitude.
- date_adjustment: Adjusts dates for sun phase transitions across midnight.
- calculate_temp: Calculates screen temperature based on current sun position.

Dependencies:
- datetime: For time and date operations.
- requests: For making HTTP requests to the sunrise-sunset API.

Note: This module requires an active internet connection to fetch sun times.
"""

from datetime import datetime, timedelta, timezone, time
import requests


def get_sun_times(lat, lng):
    """Fetches user's sun phase times for given coordinates.

    Args:
    lat (float): User's latitude
    lng (float): User's longitude

    Returns:
    dict: Contains timezone-aware datetime.time objects for four sun phases: sunrise, sunset,
    morning_twilight, night_twilight

    Raises:
    ValueError: If coordinates are invalid or API response format is incorrect
    RuntimeError: If API request fails or response processing fails
    """
    # Input validation for latitude and longitude
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
        raise ValueError("Latitude and longitude must be numbers")

    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")

    if lng < -180 or lng > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")

    base_url = "https://api.sunrise-sunset.org/json?"
    url = f"{base_url}lat={lat}&lng={lng}"

    # Attempt to connect to API, read JSON time dictionary response, and validate response
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching sun times: {e}") from e

    try:
        time_dict = response.json()
    except ValueError as e:
        raise RuntimeError(f"Error parsing JSON response: {e}") from e

    if "results" not in time_dict:
        raise requests.RequestException(
            "Invalid API response format: 'results' key missing"
        )

    time_dict = time_dict["results"]

    # Extract and validate required keys from the API response
    required_keys = ["sunrise", "sunset", "civil_twilight_begin", "civil_twilight_end"]
    for key in required_keys:
        if key not in time_dict:
            raise RuntimeError(f"Invalid API response format: '{key}' key missing")

    # Parse time strings and create sun_times dictionary
    try:
        sun_times = {
            "sunrise": datetime.strptime(time_dict["sunrise"], "%I:%M:%S %p").time(),
            "sunset": datetime.strptime(time_dict["sunset"], "%I:%M:%S %p").time(),
            "morning_twilight": datetime.strptime(
                time_dict["civil_twilight_begin"], "%I:%M:%S %p"
            ).time(),
            "night_twilight": datetime.strptime(
                time_dict["civil_twilight_end"], "%I:%M:%S %p"
            ).time(),
        }
    except (ValueError, KeyError) as e:
        raise RuntimeError(f"Error processing sun times: {e}") from e

    return sun_times


def date_adjustment(lat, lng):
    """Adjusts date if sun phase transition crosses midnight

    Since dates are not provided by the API, all times are combined with the current date. This
    causes an issue if there is a transition across midnight between two sun phases. For example, if
    sunrise is at 12:30 AM and morning twilight is at 11:30 PM, since we set them to the same day,
    sunrise will actually be before morning twilight, and this has to be incremented by one day.

    Args:
    lat: User's latitude (float)
    lng: User's longitude (float)

    Returns:
    Five datetime.datetime() objects: user_time, sunrise, sunset, morning_twilight, night_twilight,
    mpe, mpb

    Raises:
    RuntimeError: If there's an error getting user time, sun times, or adjusting dates
    KeyError: If required keys are missing in the sun_times dictionary
    """
    # Get current UTC time
    try:
        user_time = datetime.now(timezone.utc)
    except Exception as e:
        raise RuntimeError(f"Error getting user time: {e}") from e

    # Fetch sun times
    try:
        sun_times = get_sun_times(lat, lng)
    except Exception as e:
        raise RuntimeError(f"Error getting sun times: {e}") from e

    # Validate sun_times directory
    required_keys = ["sunrise", "sunset", "morning_twilight", "night_twilight"]
    for key in required_keys:
        if key not in sun_times:
            raise KeyError(f"Missing key in sun_times: '{key}'")

    # Combine sun times with current date
    today = user_time.date()
    sunrise = datetime.combine(today, sun_times["sunrise"], tzinfo=timezone.utc)
    sunset = datetime.combine(today, sun_times["sunset"], tzinfo=timezone.utc)
    morning_twilight = datetime.combine(
        today, sun_times["morning_twilight"], tzinfo=timezone.utc
    )
    night_twilight = datetime.combine(
        today, sun_times["night_twilight"], tzinfo=timezone.utc
    )

    # Increment times which are out of order, including user time
    if sunrise < morning_twilight:
        if time(00, 00) <= user_time.time() < sunrise.time():
            user_time += timedelta(days=1)
        sunrise += timedelta(days=1)
        sunset += timedelta(days=1)
        night_twilight += timedelta(days=1)

    if sunset < sunrise:
        if time(00, 00) <= user_time.time() < night_twilight.time():
            user_time += timedelta(days=1)
        sunset += timedelta(days=1)
        night_twilight += timedelta(days=1)

    if night_twilight < sunset:
        if time(00, 00) <= user_time.time() < night_twilight.time():
            user_time += timedelta(days=1)
        night_twilight += timedelta(days=1)

    # Calculate midday period start and end based on incremented times
    mpb = sunrise + (sunrise - morning_twilight)
    mpe = sunset - (night_twilight - sunset)

    # Increment mpe and mpb if out of order
    if mpb < sunrise or mpb < morning_twilight:
        mpb += timedelta(days=1)

    if mpe < mpb:
        mpe += timedelta(days=1)

    return (
        user_time,
        sunrise,
        sunset,
        morning_twilight,
        night_twilight,
        mpe,
        mpb,
    )


def calculate_temp(lat, lng):
    """Calculates what the screen temperature should be based on the user's current sun position

    The temperature ranges from 2700K to 6000K, depending on the time of day:
    - 2700K before morning twilight or after night twilight
    - 6000K between one twilight after sunrise to one twilight before sunset
    - Linear interpolation during twilight periods

    Args:
    lat: User's latitude (float)
    lng: User's longitude (float)

    Returns:
    An int/float representing the calculated screen temperature.

    Raises:
    RuntimeError: If date adjustment fails or temperature calculation encounters errors
    """
    # Constants for temperature range
    high_temp = 6000
    low_temp = 2700

    try:
        # Get adjusted times for sun phase
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(lat, lng)
        )
    except Exception as e:
        raise RuntimeError(f"Error in date adjustment: {e}") from e

    # Calculate twilight periods
    morning_twilight_length = sunrise - morning_twilight
    night_twilight_length = night_twilight - sunset

    # Figure out where the user is and return the valid temperature
    try:
        if mpb < user_time < mpe:
            return high_temp

        if morning_twilight <= user_time <= mpb:
            # Linear interpolation during morning twilight
            percent_into_twilight = (user_time - morning_twilight) / (
                2 * morning_twilight_length
            )
            return low_temp + (high_temp - low_temp) * percent_into_twilight

        if mpe <= user_time <= night_twilight:
            # Linear interpolation during evening twilight
            percent_into_twilight = (user_time - mpe) / (2 * night_twilight_length)
            return high_temp - (high_temp - low_temp) * percent_into_twilight

        return low_temp
    except TypeError as e:
        raise RuntimeError(f"Type error in calculating temperature: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Value error in calculating temperature: {e}") from e
