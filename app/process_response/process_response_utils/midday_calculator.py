from datetime import timedelta
from abc import ABC, abstractmethod


class AbstractMiddayPeriodCalculator:
    @abstractmethod
    def calculate_midday_period(self, sun_times):
        pass

    @abstractmethod
    def midday_period_adjustment(self, sun_times):
        pass

    def calculate_and_adjust_midday_periods(self, sun_times):
        response_with_midday_period = self.calculate_midday_period(sun_times)
        response_with_adjusted_midday_period = self.midday_period_adjustment(
            response_with_midday_period
        )

        return response_with_adjusted_midday_period


class MiddayPeriodCalculator(AbstractMiddayPeriodCalculator):
    def calculate_midday_period(self, sun_times):
        sun_times.midday_period_begins = sun_times.sunrise + (
            sun_times.sunrise - sun_times.morning_twilight
        )
        sun_times.midday_period_ends = sun_times.sunset - (
            sun_times.night_twilight - sun_times.sunset
        )

        return sun_times

    @staticmethod
    def midday_period_adjustment(self, sun_times):
        # Increment morning_period_end and midday_period_begins if out of order
        if (
            sun_times.midday_period_begins < sun_times.sunrise
            or sun_times.midday_period_begins < sun_times.morning_twilight
        ):
            sun_times.midday_period_begins += timedelta(days=1)

        if sun_times.midday_period_ends < sun_times.midday_period_begins:
            sun_times.midday_period_ends += timedelta(days=1)

        return sun_times
