from flask import request, jsonify
from .main import main


def register_routes(app):
    @app.route("/night-time-temperature", methods=["GET"])
    def night_time_temperature_route():
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)

        return main(lat, lng)
