from .calculate_temp_utils.get_temp import GetTemp


class CalculateTemp:
    @staticmethod
    def calculate_temp(sun_times):
        temp_calculator = GetTemp()
        return temp_calculator.get_temp(sun_times)
