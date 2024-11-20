from datetime import datetime, timezone
from .sun_times import SunTimes
from abc import ABC, abstractmethod


class AbstractResponseHandler(ABC):
    @abstractmethod
    def extract_times_from_API_response(self, raw_api_response):
        pass

    @abstractmethod
    def parse_sun_times(self, times_as_strings):
        pass

    @abstractmethod
    def combine_times_with_date(self, sun_times):
        pass

    def handle_response(self, raw_api_response):
        string_sun_times = self.extract_times_from_API_response(raw_api_response)
        sun_times = self.parse_sun_times(string_sun_times)
        sun_times_with_dates = self.combine_times_with_date(sun_times)
        return sun_times_with_dates


class ResponseHandler(AbstractResponseHandler):
    def extract_times_from_API_response(self, raw_api_response):
        return raw_api_response.json()["results"]

    def parse_sun_times(self, times_as_strings):
        return SunTimes(
            sunrise=datetime.strptime(
                times_as_strings["sunrise"], "%I:%M:%S %p"
            ).time(),
            sunset=datetime.strptime(times_as_strings["sunset"], "%I:%M:%S %p").time(),
            morning_twilight=datetime.strptime(
                times_as_strings["civil_twilight_begin"], "%I:%M:%S %p"
            ).time(),
            night_twilight=datetime.strptime(
                times_as_strings["civil_twilight_end"], "%I:%M:%S %p"
            ).time(),
        )

    def combine_times_with_date(self, sun_times):
        # Combine sun times with current date
        sun_times.user_time = datetime.now(timezone.utc)
        today = sun_times.user_time.date()
        sun_times.sunrise = datetime.combine(
            today, sun_times.sunrise, tzinfo=timezone.utc
        )
        sun_times.sunset = datetime.combine(
            today, sun_times.sunset, tzinfo=timezone.utc
        )
        sun_times.morning_twilight = datetime.combine(
            today, sun_times.morning_twilight, tzinfo=timezone.utc
        )
        sun_times.night_twilight = datetime.combine(
            today, sun_times.night_twilight, tzinfo=timezone.utc
        )

        return sun_times
