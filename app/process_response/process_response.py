from .process_response_utils.process_times import (
    ReseponseHandler,
    DateAdjustment,
    MiddayPeriodCalculations,
)
from .process_response_utils.sun_times import SunTimesAPI


class ProcessAPICall:

    @staticmethod
    def process_api_call(lat, lng):
        response = SunTimesAPI.fetch_sun_times(lat, lng)

        formatted_response = ReseponseHandler.handle_response(response)
        date_adjusted_response = DateAdjustment.adjust_dates(formatted_response)
        processed_response = (
            MiddayPeriodCalculations.calculate_and_adjust_midday_periods(
                date_adjusted_response
            )
        )
        return processed_response
