from .calculate_temp_utils.get_temp import GetTemp
from app.sun_times import SunTimes


class CalculateTemp:
    @staticmethod
    def calculate_temp(sun_times: SunTimes) -> int:
        temp_calculator = GetTemp()
        return temp_calculator.get_temp(sun_times)
