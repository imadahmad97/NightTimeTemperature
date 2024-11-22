from .get_user_time_interval import TimeIntervalCalculator
from flask import current_app
from abc import ABC, abstractmethod
from app.sun_times import SunTimes


class AbstractGetTemp(ABC):
    @abstractmethod
    def user_in_midday_period(self) -> int:
        pass

    @abstractmethod
    def user_in_night_period(self) -> int:
        pass

    @abstractmethod
    def user_in_morning_twilight(self, sun_times: SunTimes) -> int:
        pass

    @abstractmethod
    def user_in_night_twilight(self, sun_times: SunTimes) -> int:
        pass

    def get_temp(self, sun_times: SunTimes) -> int:
        if (
            sun_times.midday_period_begins
            < sun_times.user_time
            < sun_times.midday_period_ends
        ):
            return self.user_in_midday_period()
        elif (
            sun_times.morning_twilight
            <= sun_times.user_time
            <= sun_times.midday_period_begins
        ):
            return self.user_in_morning_twilight(sun_times)
        elif (
            sun_times.midday_period_ends
            <= sun_times.user_time
            <= sun_times.night_twilight
        ):
            return self.user_in_night_twilight(sun_times)
        else:
            return self.user_in_night_period()


class GetTemp(AbstractGetTemp):
    def __init__(self):
        self.time_calculator = TimeIntervalCalculator()

    def user_in_midday_period(self) -> int:
        return current_app.config["HI_TEMP"]

    def user_in_night_period(self) -> int:
        return current_app.config["LO_TEMP"]

    def user_in_morning_twilight(self, sun_times: SunTimes) -> int:
        proportion_of_twilight_complete = self.time_calculator.get_user_prop_morning(
            sun_times
        )

        return round(
            current_app.config["LO_TEMP"]
            + (current_app.config["HI_TEMP"] - current_app.config["LO_TEMP"])
            * proportion_of_twilight_complete
        )

    def user_in_night_twilight(self, sun_times: SunTimes) -> int:
        proportion_of_twilight_complete = self.time_calculator.get_user_prop_night(
            sun_times
        )

        return round(
            current_app.config["HI_TEMP"]
            - (current_app.config["HI_TEMP"] - current_app.config["LO_TEMP"])
            * proportion_of_twilight_complete
        )
