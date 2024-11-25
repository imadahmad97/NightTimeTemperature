"""
Configuration module for NightTimeTemperature.

Constants:
----------
SUNRISE_SUNSET_API_BASE_URL : str
    The base URL for the Sunrise-Sunset API used to fetch sun position data.
    
LO_TEMP : int
    The lower temperature (in Kelvin) representing the screen brightness 
    during night-time.

HI_TEMP : int
    The higher temperature (in Kelvin) representing the screen brightness 
    during daytime.
"""

SUNRISE_SUNSET_API_BASE_URL = "https://api.sunrise-sunset.org/json?"
LO_TEMP = 2700
HI_TEMP = 6000
PROFILE = "Pr"
