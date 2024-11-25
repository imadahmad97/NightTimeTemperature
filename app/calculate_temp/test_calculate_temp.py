"""
This module provides unit tests for the calculate_temp method in the CalculateTemp class.

The CalculateTemp class is responsible for calculating the temperature based on the user's input 
time.

Tests:
    - test_midday_period: Tests that the temperature is correctly calculated during the midday
      period.
    - test_night_period: Tests that the temperature is correctly calculated during the night period.   
    - test_morning_twilight_period: Tests that the temperature is correctly calculated during the
      morning twilight period.
    - test_night_twilight_period: Tests that the temperature is correctly calculated during the 
      night twilight period."""

import unittest
from datetime import datetime
from flask import Flask
from app.sun_times import SunTimes
from app.calculate_temp.calculate_temp import CalculateTemp


class TestCalculateTemp(unittest.TestCase):
    """
    Unit tests for the calculate_temp method.

    This test suite includes tests to verify that the calculate_temp method correctly calculates the
    temperature based on the user's input time and the sun times data.

    Methods:
        - setUp: Creates a SunTimes object with real values.
        - test_midday_period: Tests that the temperature is correctly calculated during the midday
          period.
        - test_night_period: Tests that the temperature is correctly calculated during the night
          period.
        - test_morning_twilight_period: Tests that the temperature is correctly calculated during
          the morning twilight period.
        - test_night_twilight_period: Tests that the temperature is correctly calculated during the
          night twilight period.
    """

    def setUp(self):
        """
        Set up the test case with a SunTimes object containing real values. This object will be used
        in the test methods to verify that the calculate_temp method correctly calculates the
        temperature based on the user's input time and the sun times data.
        """
        # Create a SunTimes object with real values
        self.app = Flask(__name__)
        self.app.config.from_pyfile("../../config.py")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.sun_times = SunTimes()
        self.sun_times.sunrise = datetime(2024, 1, 1, 6, 0)
        self.sun_times.sunset = datetime(2024, 1, 1, 18, 0)
        self.sun_times.morning_twilight = datetime(2024, 1, 1, 5, 30)
        self.sun_times.night_twilight = datetime(2024, 1, 1, 18, 30)
        self.sun_times.midday_period_begins = datetime(2024, 1, 1, 6, 30)
        self.sun_times.midday_period_ends = datetime(2024, 1, 1, 17, 30)

    def test_midday_period(self):
        """
        Test that the temperature is correctly calculated during the midday period.
        """
        # Call the method under test using the actual TimeIntervalCalculator
        self.sun_times.user_time = datetime(2024, 1, 1, 16, 0)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)

        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, 6000
        )  # Adjust expected value based on real logic

    def test_night_period(self):
        """
        Test that the temperature is correctly calculated during the night period.
        """
        self.sun_times.user_time = datetime(2024, 1, 1, 3, 30)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)

        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, 2700
        )  # Adjust expected value based on real logic

    def test_morning_twilight_period(self):
        """
        Test that the temperature is correctly calculated during the morning twilight period.
        """
        self.sun_times.user_time = datetime(2024, 1, 1, 5, 45)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)
        expected_temp = self.app.config["LO_TEMP"] + (
            self.app.config["HI_TEMP"] - self.app.config["LO_TEMP"]
        ) * (1 / 4)
        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, expected_temp
        )  # Adjust expected value based on real logic

    def test_night_twilight_period(self):
        """
        Test that the temperature is correctly calculated during the night twilight period.
        """
        self.sun_times.user_time = datetime(2024, 1, 1, 17, 45)

        calculated_temp = CalculateTemp.calculate_temp(self.sun_times)
        expected_temp = self.app.config["HI_TEMP"] - (
            self.app.config["HI_TEMP"] - self.app.config["LO_TEMP"]
        ) * (1 / 4)
        # Assert that the temperature is correctly calculated
        self.assertEqual(
            calculated_temp, expected_temp
        )  # Adjust expected value based on real logic


if __name__ == "__main__":
    unittest.main()
