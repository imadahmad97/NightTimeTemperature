from datetime import datetime, timedelta, timezone, time
from .sun_times import SunTimes, SunTimesAPI


class ReseponseHandler:
    @staticmethod
    def extract_times_from_API_response(raw_api_response):
        return raw_api_response.json()["results"]

    @staticmethod
    def parse_sun_times(times_as_strings):
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

    @staticmethod
    def combines_times_with_date(sun_times):
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

    @staticmethod
    def handle_response(raw_api_response):
        string_sun_times = ReseponseHandler.extract_times_from_API_response(
            raw_api_response
        )
        sun_times = ReseponseHandler.parse_sun_times(string_sun_times)
        sun_times_with_dates = ReseponseHandler.combines_times_with_date(sun_times)
        return sun_times_with_dates


class DateAdjustment:
    @staticmethod
    def sunrise_before_twilight(sun_times):
        if time(00, 00) <= sun_times.user_time.time() < sun_times.unrise.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunrise += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    @staticmethod
    def sunset_before_sunrise(sun_times):
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.sunset += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    @staticmethod
    def night_twilight_before_sunset(sun_times):
        if time(00, 00) <= sun_times.user_time.time() < sun_times.night_twilight.time():
            sun_times.user_time += timedelta(days=1)
        sun_times.night_twilight += timedelta(days=1)

        return sun_times

    @staticmethod
    def adjust_dates(sun_times):
        if sun_times.sunrise < sun_times.morning_twilight:
            sun_times = DateAdjustment.sunrise_before_twilight(sun_times)

        if sun_times.sunset < sun_times.sunrise:
            sun_times = DateAdjustment.sunset_before_sunrise(sun_times)

        if sun_times.night_twilight < sun_times.sunset:
            sun_times.user_time, sun_times.night_twilight = (
                DateAdjustment.night_twilight_before_sunset(sun_times)
            )

        return sun_times


class MiddayPeriodCalculations:
    @staticmethod
    def calculate_midday_period(sun_times):
        sun_times.midday_period_begins = sun_times.sunrise + (
            sun_times.sunrise - sun_times.morning_twilight
        )
        sun_times.midday_period_ends = sun_times.sunset - (
            sun_times.night_twilight - sun_times.sunset
        )

        return sun_times

    @staticmethod
    def midday_period_adjustment(sun_times):
        # Increment morning_period_end and midday_period_begins if out of order
        if (
            sun_times.midday_period_begins < sun_times.sunrise
            or sun_times.midday_period_begins < sun_times.morning_twilight
        ):
            sun_times.midday_period_begins += timedelta(days=1)

        if sun_times.midday_period_ends < sun_times.midday_period_begins:
            sun_times.midday_period_ends += timedelta(days=1)

        return sun_times

    @staticmethod
    def calculate_and_adjust_midday_periods(sun_times):
        response_with_midday_period = MiddayPeriodCalculations.calculate_midday_period(
            sun_times
        )
        response_with_adjusted_midday_period = (
            MiddayPeriodCalculations.midday_period_adjustment(
                response_with_midday_period
            )
        )

        return response_with_adjusted_midday_period
