import requests


class Validator:
    @staticmethod
    def validate_coordinates(lat, lng):
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            raise ValueError("Latitude and longitude must be numbers")

        if lat < -90 or lat > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")

        if lng < -180 or lng > 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")

    @staticmethod
    def validate_sun_times(sun_times):
        required_attributes = [
            "sunrise",
            "sunset",
            "morning_twilight",
            "night_twilight",
            "midday_period_begins",
            "midday_period_ends",
        ]
        for attr in required_attributes:
            if not hasattr(sun_times, attr):
                raise AttributeError(f"Missing attribute in sun_times: '{attr}'")

    @staticmethod
    def validate_response(time_dict):
        if "results" not in time_dict:
            raise requests.RequestException(
                "Invalid API response format, 'results' key missing"
            )
        return time_dict["results"]
