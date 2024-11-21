from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from app.sun_times import SunTimes


class AbstractTimeIntervalCalculator(ABC):
    @staticmethod
    @abstractmethod
    def calculate_user_proportion(
        user_time: datetime, start_time: datetime, interval_length: timedelta
    ) -> float:
        pass

    @abstractmethod
    def get_user_prop_morning(self, sun_times: SunTimes) -> float:
        pass

    @abstractmethod
    def get_user_prop_night(self, sun_times: SunTimes) -> float:
        pass


class TimeIntervalCalculator(AbstractTimeIntervalCalculator):
    @staticmethod
    def calculate_user_proportion(
        user_time: datetime, start_time: datetime, interval_length: timedelta
    ) -> float:
        return (user_time - start_time) / (2 * interval_length)

    def get_user_prop_morning(self, sun_times: SunTimes) -> float:
        morning_twilight_length = sun_times.sunrise - sun_times.morning_twilight
        return self.calculate_user_proportion(
            sun_times.user_time,
            sun_times.morning_twilight,
            morning_twilight_length,
        )

    def get_user_prop_night(self, sun_times: SunTimes) -> float:
        night_twilight_length = sun_times.night_twilight - sun_times.sunset
        return self.calculate_user_proportion(
            sun_times.user_time,
            sun_times.midday_period_ends,
            night_twilight_length,
        )
