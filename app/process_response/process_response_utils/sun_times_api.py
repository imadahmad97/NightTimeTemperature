import requests
from flask import current_app


class SunTimesAPI:

    @staticmethod
    def fetch_sun_times(lat: float, lng: float) -> requests.models.Response:
        url = f"{current_app.config['SUNRISE_SUNSET_API_BASE_URL']}lat={lat}&lng={lng}"
        response = requests.get(url, timeout=20)
        return response
