import requests


class SunTimes:
    def __init__(
        self,
        sunrise,
        sunset,
        morning_twilight,
        night_twilight,
        midday_period_begins=None,
        midday_period_ends=None,
        user_time=None,
    ):
        self.sunrise = sunrise
        self.sunset = sunset
        self.morning_twilight = morning_twilight
        self.night_twilight = night_twilight
        self.midday_period_begins = midday_period_begins
        self.midday_period_ends = midday_period_ends
        self.user_time = user_time


class SunTimesAPI:
    BASE_URL = "https://api.sunrise-sunset.org/json?"  # EDIT: Change to config file

    @staticmethod
    def fetch_sun_times(lat, lng):
        url = f"{SunTimesAPI.BASE_URL}lat={lat}&lng={lng}"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching sun times: {e}") from e
