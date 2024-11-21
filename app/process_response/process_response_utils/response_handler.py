from datetime import datetime
from app.sun_times import SunTimes
from abc import ABC, abstractmethod


class AbstractResponseHandler(ABC):
    @abstractmethod
    def extract_times_from_API_response(self, raw_api_response):
        pass

    @abstractmethod
    def parse_sun_times(self, times_as_strings):
        pass

    def handle_response(self, raw_api_response):
        string_sun_times = self.extract_times_from_API_response(raw_api_response)
        sun_times = self.parse_sun_times(string_sun_times)
        sun_times.set_user_time()
        sun_times.combine_times_with_date()
        return sun_times


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
