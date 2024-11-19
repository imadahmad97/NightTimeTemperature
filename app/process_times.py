from datetime import datetime, timedelta, timezone, time


class ReseponseHandler:
    @staticmethod
    def extract_times_from_API_response(raw_api_response):
        return raw_api_response.json()["results"]

    @staticmethod
    def parse_sun_times(times_as_strings):
        sun_times = {
            "sunrise": datetime.strptime(
                times_as_strings["sunrise"], "%I:%M:%S %p"
            ).time(),
            "sunset": datetime.strptime(
                times_as_strings["sunset"], "%I:%M:%S %p"
            ).time(),
            "night_twilight": datetime.strptime(
                times_as_strings["night_twilight"], "%I:%M:%S %p"
            ).time(),
            "morning_twilight": datetime.strptime(
                times_as_strings["morning_twilight"], "%I:%M:%S %p"
            ).time(),
        }
        return sun_times

    @staticmethod
    def combines_times_with_date(raw_sun_times):
        # Combine sun times with current date
        user_time = datetime.now(timezone.utc)
        today = user_time.date()
        sunrise = datetime.combine(today, raw_sun_times["sunrise"], tzinfo=timezone.utc)
        sunset = datetime.combine(today, raw_sun_times["sunset"], tzinfo=timezone.utc)
        morning_twilight = datetime.combine(
            today, raw_sun_times["morning_twilight"], tzinfo=timezone.utc
        )
        night_twilight = datetime.combine(
            today, raw_sun_times["night_twilight"], tzinfo=timezone.utc
        )

        return user_time, sunrise, sunset, morning_twilight, night_twilight

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
    def sunrise_before_twilight(user_time, sunrise, sunset, night_twilight):
        if time(00, 00) <= user_time.time() < sunrise.time():
            user_time += timedelta(days=1)
        sunrise += timedelta(days=1)
        sunset += timedelta(days=1)
        night_twilight += timedelta(days=1)

    @staticmethod
    def sunset_before_sunrise(user_time, sunset, night_twilight):
        if time(00, 00) <= user_time.time() < night_twilight.time():
            user_time += timedelta(days=1)
        sunset += timedelta(days=1)
        night_twilight += timedelta(days=1)

    @staticmethod
    def night_twilight_before_sunset(user_time, night_twilight):
        if time(00, 00) <= user_time.time() < night_twilight.time():
            user_time += timedelta(days=1)
        night_twilight += timedelta(days=1)

    @staticmethod
    def calculate_midday_period(sunrise, sunset, morning_twilight, night_twilight):
        midday_period_begins = sunrise + (sunrise - morning_twilight)
        midday_period_ends = sunset - (night_twilight - sunset)

        return midday_period_begins, midday_period_ends

    @staticmethod
    def midday_period_adjustment(
        midday_period_begins, midday_period_ends, sunrise, morning_twilight
    ):
        # Increment morning_period_end and midday_period_begins if out of order
        if midday_period_begins < sunrise or midday_period_begins < morning_twilight:
            midday_period_begins += timedelta(days=1)

        if midday_period_ends < midday_period_begins:
            midday_period_ends += timedelta(days=1)

    def adjust_date()
