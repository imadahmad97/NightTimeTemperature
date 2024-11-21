from .process_response_utils.response_handler import ResponseHandler
from .process_response_utils.midday_calculator import MiddayPeriodCalculator
from .process_response_utils.date_adjustment import DateAdjustment
from .process_response_utils.sun_times_api import SunTimesAPI


class ProcessAPICall:

    @staticmethod
    def process_api_call(lat, lng):
        response = SunTimesAPI.fetch_sun_times(lat, lng)

        response_handler = ResponseHandler()
        midday_calculator = MiddayPeriodCalculator()
        date_adjustment = DateAdjustment()

        formatted_response = response_handler.handle_response(response)
        date_adjusted_response = date_adjustment.adjust_dates(formatted_response)
        processed_response = midday_calculator.calculate_and_adjust_midday_periods(
            date_adjusted_response
        )
        return processed_response
