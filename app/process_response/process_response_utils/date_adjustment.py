from datetime import time, timedelta


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
