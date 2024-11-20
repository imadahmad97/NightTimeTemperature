from .get_user_time_interval import GetUserTimeInterval


class GetTemp:
    LO_TEMP = 2700  # Edit: Add to config
    HI_TEMP = 6000  # Edit: Add to config

    @staticmethod
    def user_in_midday_period():
        return GetTemp.HI_TEMP

    @staticmethod
    def user_in_night_period():
        return GetTemp.LO_TEMP

    @staticmethod
    def user_in_morning_twilight(sun_times):
        proportion_of_twilight_complete = GetUserTimeInterval.get_user_prop_morning(
            sun_times
        )

        return (
            GetTemp.LO_TEMP
            + (GetTemp.HI_TEMP - GetTemp.LO_TEMP) * proportion_of_twilight_complete
        )

    @staticmethod
    def user_in_night_twilight(sun_times):
        proportion_of_twilight_complete = GetUserTimeInterval.get_user_prop_night(
            sun_times
        )

        return (
            GetTemp.HI_TEMP
            - (GetTemp.HI_TEMP - GetTemp.LO_TEMP) * proportion_of_twilight_complete
        )

    @staticmethod
    def get_temp(sun_times):
        if (
            sun_times.midday_period_begins
            < sun_times.user_time
            < sun_times.midday_period_ends
        ):
            return GetTemp.user_in_midday_period()
        elif (
            sun_times.morning_twilight
            <= sun_times.user_time
            <= sun_times.midday_period_begins
        ):
            return GetTemp.user_in_morning_twilight(sun_times)
        elif (
            sun_times.midday_period_ends
            <= sun_times.user_time
            <= sun_times.night_twilight
        ):
            return GetTemp.user_in_night_twilight(sun_times)
        else:
            return GetTemp.user_in_night_period()
