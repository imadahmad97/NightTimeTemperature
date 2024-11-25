import unittest
from .process_response import ProcessAPICall
from flask import Flask
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app.sun_times import SunTimes
from freezegun import freeze_time


class TestProcessAPICall(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app.config["HI_TEMP"] = 6000
        self.app.config["LO_TEMP"] = 2700
        self.app_context.push()

    @freeze_time("2024-01-01 10:00:00", tz_offset=0)
    @patch("requests.get")  # Mock requests.get
    def test_mocked_api_response(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": {
                "sunrise": "5:00:00 AM",
                "sunset": "7:00:00 PM",
                "solar_noon": "10:00:00 PM",
                "day_length": "10:46:18",
                "civil_twilight_begin": "4:30:00 AM",
                "civil_twilight_end": "8:00:00 PM",
                "nautical_twilight_begin": "5:55:00 PM",
                "nautical_twilight_end": "2:58:54 AM",
                "astronomical_twilight_begin": "6:24:17 PM",
                "astronomical_twilight_end": "2:29:37 AM",
            },
            "status": "OK",
            "tzid": "UTC",
        }

        # Assign the mock response to requests.get
        mock_get.return_value = mock_response

        process_api = ProcessAPICall()
        # Call your function that processes the API response
        response = process_api.process_api_call(mock_response)

        expected_response = SunTimes(
            sunrise=datetime(2024, 1, 1, 5, 0, 0, tzinfo=timezone.utc),
            sunset=datetime(2024, 1, 1, 19, 0, 0, tzinfo=timezone.utc),
            morning_twilight=datetime(2024, 1, 1, 4, 30, 0, tzinfo=timezone.utc),
            night_twilight=datetime(2024, 1, 1, 20, 0, 0, tzinfo=timezone.utc),
            midday_period_begins=datetime(2024, 1, 1, 5, 30, 0, tzinfo=timezone.utc),
            midday_period_ends=datetime(2024, 1, 1, 18, 0, 0, tzinfo=timezone.utc),
            user_time=datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        )
        # Assertions
        self.assertEqual(response.sunrise, expected_response.sunrise)
        self.assertEqual(response.sunset, expected_response.sunset)
        self.assertEqual(response.morning_twilight, expected_response.morning_twilight)
        self.assertEqual(response.night_twilight, expected_response.night_twilight)
        self.assertEqual(
            response.midday_period_begins, expected_response.midday_period_begins
        )
        self.assertEqual(
            response.midday_period_ends, expected_response.midday_period_ends
        )
        self.assertEqual(response.user_time, expected_response.user_time)

    @freeze_time("2024-01-01 10:00:00", tz_offset=0)
    @patch("requests.get")  # Mock requests.get
    def test_sunrise_before_morning_twilight_adjustment(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": {
                "sunrise": "11:30:00 PM",
                "sunset": "7:00:00 PM",
                "solar_noon": "10:00:00 PM",
                "day_length": "10:46:18",
                "civil_twilight_begin": "12:30:00 AM",
                "civil_twilight_end": "8:00:00 PM",
                "nautical_twilight_begin": "5:55:00 PM",
                "nautical_twilight_end": "2:58:54 AM",
                "astronomical_twilight_begin": "6:24:17 PM",
                "astronomical_twilight_end": "2:29:37 AM",
            },
            "status": "OK",
            "tzid": "UTC",
        }

        # Assign the mock response to requests.get
        mock_get.return_value = mock_response

        process_api = ProcessAPICall()
        # Call your function that processes the API response
        response = process_api.process_api_call(mock_response)

        expected_response = SunTimes(
            sunrise=datetime(2024, 1, 1, 5, 0, 0, tzinfo=timezone.utc),
            sunset=datetime(2024, 1, 1, 19, 0, 0, tzinfo=timezone.utc),
            morning_twilight=datetime(2024, 1, 1, 4, 30, 0, tzinfo=timezone.utc),
            night_twilight=datetime(2024, 1, 1, 20, 0, 0, tzinfo=timezone.utc),
            midday_period_begins=datetime(2024, 1, 1, 5, 30, 0, tzinfo=timezone.utc),
            midday_period_ends=datetime(2024, 1, 1, 18, 0, 0, tzinfo=timezone.utc),
            user_time=datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        )
        # Assertions
        self.assertEqual(response.sunrise, expected_response.sunrise)
        self.assertEqual(response.sunset, expected_response.sunset)
        self.assertEqual(response.morning_twilight, expected_response.morning_twilight)
        self.assertEqual(response.night_twilight, expected_response.night_twilight)
        self.assertEqual(
            response.midday_period_begins, expected_response.midday_period_begins
        )
        self.assertEqual(
            response.midday_period_ends, expected_response.midday_period_ends
        )
        self.assertEqual(response.user_time, expected_response.user_time)
