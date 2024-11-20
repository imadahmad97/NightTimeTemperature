from calculate_temp_utils.get_temp import GetTemp
from process_response import ProcessAPICall


class CalculateTemp:
    def calculate_temp(sun_times):
        return GetTemp.get_temp(sun_times)


res = ProcessAPICall.process_api_call(49, -123)
print(CalculateTemp.calculate_temp(res))
