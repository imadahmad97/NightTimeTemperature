from .process_response.process_response import ProcessAPICall
from .calculate_temp.calculate_temp import CalculateTemp
from flask import jsonify


def main(lat, lng):
    processed_api_response = ProcessAPICall.process_api_call(lat, lng)
    return jsonify(temperature=CalculateTemp.calculate_temp(processed_api_response))
