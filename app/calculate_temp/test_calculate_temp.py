import unittest
from app.sun_times import SunTimes
from app.calculate_temp.calculate_temp_utils.get_user_time_interval import (
    TimeIntervalCalculator,
)
from app.calculate_temp.calculate_temp import CalculateTemp
from datetime import datetime
from flask import Flask


class TestCalculateTemp(unittest.TestCase):
    def setUp(self):
        # Create a SunTimes object with real values
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app.config["HI_TEMP"] = 6000
        self.app.config["LO_TEMP"] = 2700
        self.app_context.push()
        self.sun_times = SunTimes()
        self.sun_times.sunrise = datetime(2024, 1, 1, 6, 0)
        self.sun_times.sunset = datetime(2024, 1, 1, 18, 0)
        self.sun_times.morning_twilight = datetime(2024, 1, 1, 5, 30)
        self.sun_times.night_twilight = datetime(2024, 1, 1, 18, 30)
        self.sun_times.midday_period_begins = datetime(2024, 1, 1, 6, 30)
        self.sun_times.midday_period_ends = datetime(2024, 1, 1, 17, 30)

    def test_midday_period(self):
        # Call the method under test using the actual TimeIntervalCalculator
        self.sun_times.user_time = datetime(2024, 1, 1, 16, 0)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)

        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, 6000
        )  # Adjust expected value based on real logic

    def test_night_period(self):
        self.sun_times.user_time = datetime(2024, 1, 1, 3, 30)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)

        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, 2700
        )  # Adjust expected value based on real logic

    def morning_twilight_period(self):
        self.sun_times.user_time = datetime(2024, 1, 1, 5, 45)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)

        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, 2700
        )  # Adjust expected value based on real logic


if __name__ == "__main__":
    unittest.main()
