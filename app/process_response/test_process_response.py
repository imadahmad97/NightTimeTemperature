import unittest
from .process_response import ProcessAPICall
from flask import Flask
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app.sun_times import SunTimes
from freezegun import freeze_time
import warnings


class TestProcessAPICall(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="The '__version__' attribute is deprecated and will be removed in Werkzeug 3.1.",
        )
        self.app = Flask(__name__)
        self.app.config["HI_TEMP"] = 6000
        self.app.config["LO_TEMP"] = 2700
        self.app.config["SUNRISE_SUNSET_API_BASE_URL"] = (
            "https://api.sunrise-sunset.org/json?"
        )

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Push the request context
        self.request_context = self.app.test_request_context()
        self.request_context.push()

        self.client = self.app.test_client()

    @freeze_time("2024-01-01 10:00:00", tz_offset=0)
    @patch("requests.get")  # Mock requests.get
    def test_no_adjustments(self, mock_get):
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
        response = process_api.process_api_call()

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
                "sunrise": "12:30:00 AM",
                "sunset": "7:00:00 PM",
                "solar_noon": "10:00:00 PM",
                "day_length": "10:46:18",
                "civil_twilight_begin": "11:30:00 PM",
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
        response = process_api.process_api_call()
        expected_response = SunTimes(
            sunrise=datetime(2024, 1, 2, 0, 30, 0, tzinfo=timezone.utc),
            sunset=datetime(2024, 1, 2, 19, 0, 0, tzinfo=timezone.utc),
            morning_twilight=datetime(2024, 1, 1, 23, 30, 0, tzinfo=timezone.utc),
            night_twilight=datetime(2024, 1, 2, 20, 00, 0, tzinfo=timezone.utc),
            midday_period_begins=datetime(2024, 1, 2, 1, 30, 0, tzinfo=timezone.utc),
            midday_period_ends=datetime(2024, 1, 2, 18, 0, 0, tzinfo=timezone.utc),
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
    def test_sunset_before_sunrise_adjustment(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": {
                "sunrise": "10:30:00 PM",
                "sunset": "6:30:00 AM",
                "solar_noon": "10:00:00 PM",
                "day_length": "10:46:18",
                "civil_twilight_begin": "10:00:00 PM",
                "civil_twilight_end": "7:30:00 AM",
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
        response = process_api.process_api_call()
        expected_response = SunTimes(
            sunrise=datetime(2024, 1, 1, 22, 30, 0, tzinfo=timezone.utc),
            sunset=datetime(2024, 1, 2, 6, 30, 0, tzinfo=timezone.utc),
            morning_twilight=datetime(2024, 1, 1, 22, 0, 0, tzinfo=timezone.utc),
            night_twilight=datetime(2024, 1, 2, 7, 30, 0, tzinfo=timezone.utc),
            midday_period_begins=datetime(2024, 1, 1, 23, 0, 0, tzinfo=timezone.utc),
            midday_period_ends=datetime(2024, 1, 2, 5, 30, 0, tzinfo=timezone.utc),
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
    def test_night_twilight_before_sunset_adjustment(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": {
                "sunrise": "4:30:00 PM",
                "sunset": "11:30:00 PM",
                "solar_noon": "10:00:00 PM",
                "day_length": "10:46:18",
                "civil_twilight_begin": "3:30:00 PM",
                "civil_twilight_end": "12:30:00 AM",
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
        response = process_api.process_api_call()
        expected_response = SunTimes(
            sunrise=datetime(2024, 1, 1, 16, 30, 0, tzinfo=timezone.utc),
            sunset=datetime(2024, 1, 1, 23, 30, 0, tzinfo=timezone.utc),
            morning_twilight=datetime(2024, 1, 1, 15, 30, 0, tzinfo=timezone.utc),
            night_twilight=datetime(2024, 1, 2, 0, 30, 0, tzinfo=timezone.utc),
            midday_period_begins=datetime(2024, 1, 1, 17, 30, 0, tzinfo=timezone.utc),
            midday_period_ends=datetime(2024, 1, 1, 22, 30, 0, tzinfo=timezone.utc),
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
