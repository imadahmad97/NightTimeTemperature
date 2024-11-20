from .calculate_temp_utils.get_temp import GetTemp


class CalculateTemp:
    @staticmethod
    def calculate_temp(sun_times):
        return GetTemp.get_temp(sun_times)
