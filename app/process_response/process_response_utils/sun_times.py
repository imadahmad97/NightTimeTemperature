import requests
from datetime import datetime, timezone
from abc import ABC, abstractmethod


class AbstractSunTimes(ABC):
    @abstractmethod
    def set_user_time(self, user_time=None):
        """Sets the user time, defaulting to the current UTC time."""
        pass

    @abstractmethod
    def combine_times_with_date(self, date=None):
        """Combines sun times with a given date, defaulting to today."""
        pass

    @abstractmethod
    def __repr__(self):
        """Provides a string representation of the sun times."""
        pass


class SunTimes(AbstractSunTimes):
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

    def set_user_time(self, user_time=None):
        self.user_time = user_time or datetime.now(timezone.utc)

    def combine_times_with_date(self):
        self.set_user_time()

        date = self.user_time.date()

        self.sunrise = datetime.combine(date, self.sunrise, tzinfo=timezone.utc)
        self.sunset = datetime.combine(date, self.sunset, tzinfo=timezone.utc)
        self.morning_twilight = datetime.combine(
            date, self.morning_twilight, tzinfo=timezone.utc
        )
        self.night_twilight = datetime.combine(
            date, self.night_twilight, tzinfo=timezone.utc
        )

    def __repr__(self):
        return (
            f"SunTimes(sunrise={self.sunrise}, sunset={self.sunset}, "
            f"morning_twilight={self.morning_twilight}, night_twilight={self.night_twilight}, "
            f"midday_period_begins={self.midday_period_begins}, midday_period_ends={self.midday_period_ends}, "
            f"user_time={self.user_time})"
        )


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
