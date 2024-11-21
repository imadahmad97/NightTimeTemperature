from datetime import time, timedelta
from abc import ABC, abstractmethod
from app.sun_times import SunTimes


class AbstractDateAdjustment(ABC):
    @abstractmethod
    def sunrise_before_twilight(self, sun_times: SunTimes) -> SunTimes:
        pass

    @abstractmethod
    def sunset_before_sunrise(self, sun_times: SunTimes) -> SunTimes:
        pass

    @abstractmethod
    def night_twilight_before_sunset(self, sun_times: SunTimes) -> SunTimes:
        pass

    def adjust_dates(self, sun_times: SunTimes) -> SunTimes:

        if sun_times.sunrise < sun_times.morning_twilight:
            sun_times = self.sunrise_before_twilight(sun_times)

        if sun_times.sunset < sun_times.sunrise:
            sun_times = self.sunset_before_sunrise(sun_times)

        if sun_times.night_twilight < sun_times.sunset:
            sun_times = self.night_twilight_before_sunset(sun_times)

        return sun_times


class DateAdjustment(AbstractDateAdjustment):
    def sunrise_before_twilight(self, sun_times: SunTimes) -> SunTimes:
        if time(00, 00) <= sun_times.user_time.time() < sun_times.sunrise.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunrise += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    def sunset_before_sunrise(self, sun_times: SunTimes) -> SunTimes:
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    def night_twilight_before_sunset(self, sun_times: SunTimes) -> SunTimes:
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times
