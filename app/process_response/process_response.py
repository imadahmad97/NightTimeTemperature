from .process_response_utils.response_handler import ResponseHandler
from .process_response_utils.midday_calculator import MiddayPeriodCalculator
from .process_response_utils.date_adjustment import DateAdjustment
from .process_response_utils.sun_times_api import SunTimesAPI
from app.sun_times import SunTimes


class ProcessAPICall:

    @staticmethod
    def process_api_call(lat: float, lng: float) -> SunTimes:
        response = SunTimesAPI.fetch_sun_times(lat, lng)

        response_handler = ResponseHandler()
        sun_times_builder = SunTimes()
        midday_calculator = MiddayPeriodCalculator()
        date_adjustment = DateAdjustment()

        formatted_response = response_handler.handle_response(response)
        raw_sun_times_object = sun_times_builder.process_sun_times(formatted_response)
        date_adjusted_sun_times_object = date_adjustment.adjust_dates(
            raw_sun_times_object
        )
        processed_sun_times_object = (
            midday_calculator.calculate_and_adjust_midday_periods(
                date_adjusted_sun_times_object
            )
        )

        return processed_sun_times_object
