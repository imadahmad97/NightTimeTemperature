class GetUserTimeInterval:
    @staticmethod
    def get_user_prop_morning(sun_times):
        morning_twilight_length = sun_times.sunrise - sun_times.morning_twilight
        user_prop = (sun_times.user_time - sun_times.morning_twilight) / (
            2 * morning_twilight_length
        )

        return user_prop

    @staticmethod
    def get_user_prop_night(sun_times):
        night_twilight_length = sun_times.night_twilight - sun_times.sunset
        user_prop = (sun_times.user_time - sun_times.morning_period_ends) / (
            2 * night_twilight_length
        )

        return user_prop


6043453565
