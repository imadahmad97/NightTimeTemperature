"""Test Module for utils.py

This module contains test suites for three main methods of utils.py

1. TestGetSunTimes:
    Tests the get_sun_times function which retrieves sun event times from an external API, including
    error handling and data validation.

2. TestDateAdjustment:
    Tests the date_adjustment function which handles date boundary cases when sun events cross 
    midnight, ensuring correct date assignments.

3. TestCalculateTemp:
    Tests the calculate_temp function which determines temperature values based on the current 
    time's relationship to sun events.

Test Coverage:
    - API interaction and error handling
    - Date boundary handling around midnight
    - Temperature calculations during different parts of the day
    - Edge cases for various geographical locations
    - Input validation and error responses

Dependencies:
    unittest: Standard Python testing framework
    unittest.mock: For mocking external dependencies
    datetime: For date and time handling
    requests: For API interaction testing
    json: For JSON response handling
    .utils: Internal module being tested
"""

import unittest
from unittest.mock import patch
from datetime import datetime, time, timezone, date
import json
import requests
from app.utils import get_sun_times, date_adjustment, calculate_temp


class TestGetSunTimes(unittest.TestCase):
    """A test suite for the get_sun_times function.

    This class contains a series of unit tests to verify the functionality, error handling, and edge
    cases of the get_sun_times function.

    Attributes:
        mock_response_data (dict): A sample of valid response data used for testing.

    Test Methods:
        setUp: Initializes mock data for tests.
        test_api_call_with_correct_url: Verifies correct API URL construction.
        test_api_called_with_different_coordinates: Tests function with various coordinates.
        test_invalid_coordinates_raise_error: Checks error handling for invalid coordinates.
        test_api_error_responses: Verifies handling of different HTTP error codes.
        test_unexpected_json_structure: Tests handling of unexpected API response formats.
        test_returned_dictionary: Checks the structure and types of returned data.
        test_network_error: Verifies handling of network connection errors.
        test_invalid_json: Tests the response to invalid JSON data from the API.
    """

    def setUp(self):
        """
        Set up the test environment before each test method is run.

        This method initializes a mock response data structure that simulates a successful API
        response from the sunrise-sunset.org service.

        This setup method runs before each test, ensuring that each test starts with a fresh,
        unmodified set of mock data.
        """
        self.mock_response_data = {
            "results": {
                "sunrise": "11:00:55 AM",
                "sunset": "8:55:14 PM",
                "solar_noon": "3:58:05 PM",
                "day_length": "09:54:19",
                "civil_twilight_begin": "10:31:33 AM",
                "civil_twilight_end": "9:24:37 PM",
                "nautical_twilight_begin": "9:56:38 AM",
                "nautical_twilight_end": "9:59:32 PM",
                "astronomical_twilight_begin": "9:22:27 AM",
                "astronomical_twilight_end": "10:33:42 PM",
            },
            "status": "OK",
            "tzid": "UTC",
        }

    @patch("requests.get")
    def test_api_call_with_correct_url(self, mock_get):
        """Checks that get_sun_times is calling the correct URL and that it is called once

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - The requests.get method is called exactly once.
            - The URL used in the API call matches the expected URL.
        """
        # Arrange
        lat, lng = 51.5074, -0.1278
        expected_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}"

        # Configure the mock response to return a succesful status code and valid response data
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        # Act
        get_sun_times(lat, lng)

        # Assert: Check if the API is called once and check if the URL is what we expected
        mock_get.assert_called_once()
        actual_url = mock_get.call_args[0][0]
        self.assertEqual(actual_url, expected_url)

    @patch("requests.get")
    def test_api_called_with_different_coordinates(self, mock_get):
        """Checks that get_sun_times works with edge-case coordinates

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - The requests.get method is called exactly once.
            - The URL used in the API call matches the expected URL.
        """
        # Arrange: Create edge-case coordinate arrays
        test_coordinates = [
            (0, 0),
            (90, 0),
            (-90, 0),
            (35.6762, 139.6503),
        ]
        # Configure the mock response to return a succesful status code and valid response data
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        # Loop through test coordinates, checking that the API is succesfully called
        for lat, lng in test_coordinates:
            # Reset the mock for each test case
            mock_get.reset_mock()

            expected_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}"

            # Act
            get_sun_times(lat, lng)

            # Assert: Check API success by ensuring it's only called once and that URL's are equal
            mock_get.assert_called_once()
            actual_url = mock_get.call_args[0][0]

            self.assertEqual(
                actual_url, expected_url, f"Failed for coordinates: {lat}, {lng}"
            )

    def test_invalid_coordinates_raise_error(self):
        """Checks that get_sun_times correctly identifies invalid coordinates

        Args:
            self: The test case instance.

        Assertions:
            - A ValueError is raised for invalid coordinates
        """
        invalid_coordinates = [
            (91, 0),  # Latitude too high
            (-91, 0),  # Latitude too low
            (0, 181),  # Longitude too high
            (0, -181),  # Longitude too low
            ("abc", 0),  # Invalid type for latitude
            (0, "def"),  # Invalid type for longitude
        ]

        # Loop through invalid coordinates, ensuring a ValueError is raised for each
        for lat, lng in invalid_coordinates:
            with self.assertRaises(ValueError):
                get_sun_times(lat, lng)

    @patch("requests.get")
    def test_api_error_responses(self, mock_get):
        """Test that get_sun_times function properly handles API error responses.

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - A RequestException is raised for every error code.
        """
        # Arrange: Configure mock response to return a standard value (not throwing an error)
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"status": "ERROR"}

        # Loop through error codes to see that the API raises a RequestException for each
        error_codes = [400, 404, 500]
        for code in error_codes:
            mock_response.status_code = code
            # Act and assert
            with self.assertRaises(requests.RequestException):
                get_sun_times(0, 0)

    @patch("requests.get")
    def test_unexpected_json_structure(self, mock_get):
        """Tests get_sun_time's error handling of unexpected JSON responses from sunrise-sunset API.

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - A RequestException is raised for unexpected JSON responses from sunrise-sunset API.
        """
        # Arrange: Configure mock response to return a value (not throwing an error)
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"unexpected": "structure"}

        # Act and Assert: Check that a RequestException is raised with unexpected JSON formats
        with self.assertRaises(requests.RequestException):
            get_sun_times(0, 0)

    @patch("requests.get")
    def test_returned_dictionary(self, mock_get):
        """Tests that get_sun_times get expected keys from the sunrise-sunset API response JSO, and
        that returned values are formatted correclty.

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - Asserts that the keys are equal to our expected keys.
            - Asserts that the values returned are datetime.time objects.
        """
        # Arrange: Configure mock response to return a succesful status code and valid response data

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        # Act
        result = get_sun_times(0, 0)

        expected_keys = [
            "sunrise",
            "sunset",
            "morning_twilight",
            "night_twilight",
        ]

        # Check that returned keys are equal to expected keys
        self.assertEqual(set(result.keys()), set(expected_keys))

        # Check that returned keys are datetime.time objects
        for value in result.values():
            self.assertIsInstance(value, time)

    @patch("requests.get")
    def test_network_error(self, mock_get):
        """Tests error handling of get_sun_times when ConnectionError from sunrise-sunset

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - Assert a RuntimeError is raised when the API receives a ConnectionError.
            - Assert that the correct string is returned to the user.
        """

        # Arrange: Simulate mock connection error
        mock_get.side_effect = requests.ConnectionError()

        # Act and Assert: Assert that a RuntimeError is raised when a ConnectionError is returned
        with self.assertRaises(RuntimeError) as context:
            get_sun_times(0, 0)

        # Assert that the correct string is returned to the user
        self.assertIn("Error fetching sun times", str(context.exception))

    @patch("requests.get")
    def test_invalid_json(self, mock_get):
        """Tests error handling of get_sun_times when an invalid JSON is returned

        Args:
            self: The test case instance.
            mock_get (MagicMock): A mocked version of requests.get, injected by the patch decorator.

        Assertions:
            - Assert a RuntimeError is raised when the API receives an invalid JSON.
            - Assert that the correct string is returned to the user.
        """
        # Arrange: Simulate an invalid JSON being returned to the API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        # Act and Assert: Assert there is a RuntimeError raised when an invalid JSON is returned
        with self.assertRaises(RuntimeError) as context:
            get_sun_times(0, 0)

        # Assert that the correct string is returned to the user
        self.assertIn("Error parsing JSON response", str(context.exception))


class TestDateAdjustment(unittest.TestCase):
    """Test suite for the date_adjustment function.

    This class contains a series of unit tests to verify the functionality of the
    date_adjustment function across various scenarios, including edge cases related
    to day boundaries

    Attributes:
        sun_times (dict): A dictionary containing mock sun event times used as a base
                          for testing.
        test_date (date): A fixed date used for testing to ensure consistency across
                          test cases.

    Test Methods:
        test_no_edge_case:
            Tests the function's behavior during normal daytime hours.

        test_sunrise_before_twilight_user_before_midnight:
            Tests when sunrise is before morning twilight and user time is before midnight.

        test_sunrise_before_twilight_user_after_midnight:
            Tests when sunrise is before morning twilight and user time is after midnight.

        test_twilight_before_sunset_user_before_midnight:
            Tests when night twilight is before sunset and user time is before midnight.

        test_twilight_before_sunset_user_after_midnight:
            Tests when night twilight is before sunset and user time is after midnight.

        test_mpe_after_midnight
            Tests when the morning period ends after midnight.

        test_sunset_before_mpe
            Tests when sunset is before the mpe.

        test_sunset_before_mpe_user_before_night_twilight
            Tests when sunset is before mpe and user is before night_twilight.

        test_mpb_after_midnight
            Tests when mpb is after midnight.

    """

    def setUp(self):
        """
        Set up the test environment before each test method is run.

        This method initializes common test data used across multiple test cases.
        It sets up:
        1. A dictionary of mock sun times representing a typical day's sun events.
        2. A fixed test date to be used as a reference point in tests.
        """
        # Mock sun times data
        self.sun_times = {
            "morning_twilight": time(5, 0),  # 5:00 AM
            "sunrise": time(6, 0),  # 6:00 AM
            "sunset": time(18, 0),  # 6:00 PM
            "night_twilight": time(18, 30),  # 6:30 PM
        }
        # Mock test date
        self.test_date = date(2024, 1, 1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_no_edge_case(self, mock_get_sun_times, mock_datetime):
        """Test date_adjustment function behavior during normal daytime hours.

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        mock_get_sun_times.return_value = self.sun_times

        # Set the user time to 12:00 PM
        mock_now = datetime.combine(self.test_date, time(12, 0), tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now

        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 0),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(6, 0),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 1),
                time(18, 0),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(5, 0),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(18, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 1),
                time(17, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(7, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_sunrise_before_twilight_user_before_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test date_adjustment when sunrise before morning_twilight and user is before midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that sunrise was incremented by one day
                - Checks that sunset was incremented by one day
                - Checks that night_twilight was incremented by one day
                - mpe and mpb incremented by one day
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(23, 30)  # 11:30 PM
        edge_times["sunrise"] = time(00, 30)  # 12:30 AM
        edge_times["sunset"] = time(9, 00)  # 9:00 AM
        edge_times["night_twilight"] = time(10, 30)  # 10:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 11:45 PM
        test_time = datetime.combine(self.test_date, time(23, 45), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 45),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 2),
                time(7, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 30),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_sunrise_before_twilight_user_after_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test date_adjustment when sunrise before morning_twilight and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that sunrise was incremented by one day
                - Checks that sunset was incremented by one day
                - Checks that night_twilight was incremented by one day
                - mpe and mpb incremented by one day
                - Checks that user time was incremented by one day
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(23, 30)  # 11:30 PM
        edge_times["sunrise"] = time(00, 30)  # 12:30 AM
        edge_times["sunset"] = time(9, 00)  # 9:00 AM
        edge_times["night_twilight"] = time(10, 30)  # 10:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 12:15 AM
        test_time = datetime.combine(self.test_date, time(00, 15), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 15),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 2),
                time(7, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 30),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_twilight_before_sunset_user_before_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test date_adjustment when night_twilight before sunset and user is before midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that night_twilight was incremented by one day
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(10, 30)  # 10:30 AM
        edge_times["sunset"] = time(23, 30)  # 11:30 PM
        edge_times["night_twilight"] = time(00, 30)  # 12:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 11:45 PM
        test_time = datetime.combine(self.test_date, time(23, 45), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 45),
                tzinfo=timezone.utc,
            ),
        )

        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 1),
                time(22, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_twilight_before_sunset_user_after_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test date_adjustment when night_twilight before sunset and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that night_twilight was incremented by one day
                - Checks that user_time was incremented by one day
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(10, 30)  # 10:30 AM
        edge_times["sunset"] = time(23, 30)  # 11:30 PM
        edge_times["night_twilight"] = time(00, 30)  # 12:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 12:15 AM
        test_time = datetime.combine(self.test_date, time(00, 15), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 15),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 1),
                time(22, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_mpe_after_midnight(self, mock_get_sun_times, mock_datetime):
        """Test date_adjustment when night_twilight before sunset and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that everything after mpe is incremented
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(10, 30)  # 10:30 AM
        edge_times["sunset"] = time(2, 30)  # 2:30 AM
        edge_times["night_twilight"] = time(3, 30)  # 3:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 2:00 AM
        test_time = datetime.combine(self.test_date, time(2, 00), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 2),
                time(2, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(2, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(3, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_sunset_before_mpe(self, mock_get_sun_times, mock_datetime):
        """Test date_adjustment when night_twilight before sunset and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that everything after mpe is incremented
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(10, 30)  # 10:30 AM
        edge_times["sunset"] = time(0, 30)  # 12:30 AM
        edge_times["night_twilight"] = time(1, 30)  # 1:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 2:00 AM
        test_time = datetime.combine(self.test_date, time(2, 00), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 1),
                time(2, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(0, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_sunset_before_mpe_user_before_night_twilight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test date_adjustment when night_twilight before sunset and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that everything after mpe is incremented
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(10, 30)  # 10:30 AM
        edge_times["sunset"] = time(0, 30)  # 12:30 AM
        edge_times["night_twilight"] = time(1, 30)  # 1:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 1:15 AM
        test_time = datetime.combine(self.test_date, time(1, 15), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 15),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(0, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(9, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(1, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 1),
                time(12, 00),
                tzinfo=timezone.utc,
            ),
        )

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_mpb_after_midnight(self, mock_get_sun_times, mock_datetime):
        """Test date_adjustment when night_twilight before sunset and user is after midnight .

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that all returned datetime objects have:
            - Correct date
                - Checks that everything after mpb is incremented
            - Correct times for:
            - Correct timezone (UTC)
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(23, 00)  # 11:00 PM
        edge_times["sunrise"] = time(23, 45)  # 11:45 PM
        edge_times["sunset"] = time(9, 00)  # 9:00 AM
        edge_times["night_twilight"] = time(10, 30)  # 10:30 AM
        mock_get_sun_times.return_value = edge_times

        # Set the current user time to 12:00 AM
        test_time = datetime.combine(self.test_date, time(00, 00), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        user_time, sunrise, sunset, morning_twilight, night_twilight, mpe, mpb = (
            date_adjustment(0, 0)
        )

        # Assert: Check that response times are equal to what we expect
        self.assertEqual(
            user_time,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunrise,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 45),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            sunset,
            datetime.combine(
                date(2024, 1, 2),
                time(9, 0),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            morning_twilight,
            datetime.combine(
                date(2024, 1, 1),
                time(23, 00),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            night_twilight,
            datetime.combine(
                date(2024, 1, 2),
                time(10, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpe,
            datetime.combine(
                date(2024, 1, 2),
                time(7, 30),
                tzinfo=timezone.utc,
            ),
        )
        self.assertEqual(
            mpb,
            datetime.combine(
                date(2024, 1, 2),
                time(00, 30),
                tzinfo=timezone.utc,
            ),
        )


class TestCalulculateTemp(unittest.TestCase):
    """
    Test suite for the calculate_temp function.

    This class contains a series of unit tests to verify the functionality of the
    calculate_temp function across various scenarios, including normal day/night
    cycles and edge cases involving day boundaries.

    Attributes:
        sun_times (dict): Mock sun times data used across tests.
        hi_temp (int): Constant representing the highest temperature.
        lo_temp (int): Constant representing the lowest temperature.
        test_date (date): Mock date used for testing.

    Test Methods:
        test_midday_returns_high_temp:
            Verifies that midday returns the highest temperature.

        test_night_returns_low_temp:
            Checks that nighttime returns the lowest temperature.

        test_morning_twilight_transition:
            Tests temperature calculation during morning twilight.

        test_evening_twilight_transition:
            Tests temperature calculation during evening twilight.

        test_edge_case_midnight_crossing_sunset:
            Verifies correct temperature when sunset crosses midnight.

        test_edge_case_midnight_crossing_sunrise:
            Checks temperature calculation when sunrise is after midnight.

        test_edge_case_sunset_twilight_after_midnight:
            Tests scenario where sunset and night twilight are after midnight.
    """

    def setUp(self):
        """
        Set up the test environment before each test method is run.

        This method initializes mock data and constants used across multiple test cases:
        1. sun_times: A dictionary of mock sun event times for a typical day.
        2. hi_temp and lo_temp: Constants representing the temperature range.
        3. test_date: A fixed date used for consistent testing.
        """
        # Mock sun times data
        self.sun_times = {
            "sunrise": time(6, 0),  # 6:00 AM
            "sunset": time(18, 0),  # 6:00 PM
            "morning_twilight": time(5, 0),  # 5:00 AM
            "night_twilight": time(18, 30),  # 6:30 PM
        }

        # Constants
        self.hi_temp = 6000
        self.lo_temp = 2700

        # Mock Test date
        self.test_date = date(2024, 1, 1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_midday_returns_high_temp(self, mock_get_sun_times, mock_datetime):
        """Test calculate_temp between (sunrise + twilight_length) and (sunset - twilight_length).

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to hi_temp
        """
        # Arrange: Configure mock responses with valid data and current time
        mock_get_sun_times.return_value = self.sun_times

        # Test at noon
        mock_datetime.now.return_value = datetime.combine(
            self.test_date, time(12, 0), tzinfo=timezone.utc
        )

        # Act
        result = calculate_temp(0, 0)

        # Assert: Verifies hi_temp is returned
        self.assertEqual(result, self.hi_temp)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_night_returns_low_temp(self, mock_get_sun_times, mock_datetime):
        """Test calculate_temp during night time between sunrise and sunset.

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to lo_temp
        """
        # Arrange: Configure mock responses with valid data and current time
        mock_get_sun_times.return_value = self.sun_times

        # Test at 3 AM
        mock_datetime.now.return_value = datetime.combine(
            self.test_date, time(3, 0), tzinfo=timezone.utc
        )

        # Act
        result = calculate_temp(0, 0)

        # Assert: Verifies lo_temp is returned
        self.assertEqual(result, self.lo_temp)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_morning_twilight_transition(self, mock_get_sun_times, mock_datetime):
        """Test calculate_temp between morning_twilight and sunrise.

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 1/8 of lo_temp + (hi_temp - lo_temp)
        """
        # Arrange: Configure mock responses with valid data and current time
        mock_get_sun_times.return_value = self.sun_times

        # Test at 5:15 AM
        mock_datetime.now.return_value = datetime.combine(
            self.test_date, time(5, 15), tzinfo=timezone.utc
        )

        # Act
        result = calculate_temp(0, 0)

        # Assert: At 5:15 AM, we're 15 minutes into a 120-minute twilight period, so we're 1/8
        # through the transition from low to high temp
        expected_temp = self.lo_temp + (self.hi_temp - self.lo_temp) * (1 / 8)
        self.assertAlmostEqual(result, expected_temp, places=1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_evening_twilight_transition(self, mock_get_sun_times, mock_datetime):
        """Test calculate_temp between sunset and night_twilight.

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 3/4 of hi_temp - (hi_temp - lo_temp)
        """
        # Arrange: Configure mock responses with valid data and current time
        mock_get_sun_times.return_value = self.sun_times

        # Test at 6:15 PM
        mock_datetime.now.return_value = datetime.combine(
            self.test_date, time(18, 15), tzinfo=timezone.utc
        )

        # Act
        result = calculate_temp(0, 0)

        # Assert: At 6:15 PM, we're 45 minutes into a 60-minute twilight period, so we're 3/4
        # through the transition from high to low temp
        twilight_progress = 3 / 4
        expected_temp = self.hi_temp - (self.hi_temp - self.lo_temp) * twilight_progress
        self.assertAlmostEqual(result, expected_temp, places=1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_edge_case_midnight_crossing_sunset(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test calculate_temp between sunset and night_twilight when user_time and night_twilight
        after midnight

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 11/12 of
            hi_temp - (hi_temp - lo_temp), meaning user_time and night_twilight incremented
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 00)  # 9:00 AM
        edge_times["sunrise"] = time(9, 30)  # 9:30 AM
        edge_times["sunset"] = time(23, 00)  # 11:00 PM
        edge_times["night_twilight"] = time(0, 30)  # 12:30 AM
        mock_get_sun_times.return_value = edge_times

        # Test at 12:15 AM
        test_time = datetime.combine(self.test_date, time(0, 15), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        result = calculate_temp(0, 0)

        # Assert: Calculate expected temperature at 12:15 AM, we're 75 minutes into a 90-minute
        # twilight period, so we're 11/12 through the transition from high to low temp
        twilight_progress = 11 / 12
        expected_temp = self.hi_temp - (self.hi_temp - self.lo_temp) * (
            twilight_progress
        )
        self.assertAlmostEqual(result, expected_temp, places=1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_edge_case_midnight_crossing_sunrise(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test calculate_temp between morning_twilight and sunrise when user_time and sunrise
        after midnight

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 3/8 of lo_temp + (hi_temp - lo_temp),
            meaning user_time and sunrise incremented
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(23, 30)  # 11:30 PM
        edge_times["sunrise"] = time(0, 30)  # 12:30 AM
        edge_times["sunset"] = time(9, 00)  # 9:00 AM
        edge_times["night_twilight"] = time(10, 30)  # 10:30 AM
        mock_get_sun_times.return_value = edge_times

        # Test at 12:15 AM
        test_time = datetime.combine(self.test_date, time(0, 15), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        result = calculate_temp(0, 0)

        # Assert: Calculate expected temperature at 12:15 AM, we're 45 minutes into a 120-minute
        # twilight period, so we're 3/8 through the transition from high to low temp
        twilight_progress = 3 / 8
        expected_temp = self.lo_temp + (self.hi_temp - self.lo_temp) * (
            twilight_progress
        )
        self.assertAlmostEqual(result, expected_temp, places=1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_edge_case_sunset_twilight_after_midnight_user_before_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test calculate_temp between sunset and night_twilight when user_time, sunset, and
        night_twilight after midnight

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 5/8 of hi_temp + (lo_temp - lo_temp),
            meaning user_time, sunset, and night_twilight incremented
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 30)  # 9:30 AM
        edge_times["sunrise"] = time(11, 30)  # 11:30 AM
        edge_times["sunset"] = time(00, 30)  # 12:30 AM
        edge_times["night_twilight"] = time(1, 30)  # 1:30 AM
        mock_get_sun_times.return_value = edge_times

        # Test at 12:45 AM
        test_time = datetime.combine(self.test_date, time(23, 45), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        result = calculate_temp(0, 0)

        # Assert: Calculate expected temperature at 12:45 AM, we're 15 minutes into a 120-minute
        # twilight period, so we're 1/8 through the transition from high to low temp
        twilight_progress = 1 / 8
        expected_temp = self.hi_temp - (self.hi_temp - self.lo_temp) * (
            twilight_progress
        )
        self.assertAlmostEqual(result, expected_temp, places=1)

    @patch("app.utils.datetime", wraps=datetime)
    @patch("app.utils.get_sun_times")
    def test_edge_case_sunset_twilight_after_midnight_user_after_midnight(
        self, mock_get_sun_times, mock_datetime
    ):
        """Test calculate_temp between sunset and night_twilight when user_time, sunset, and
        night_twilight after midnight

        Args:
            self: The test case instance
            mock_get_sun_times (MagicMock): Mock for the get_sun_times function
            mock_datetime (MagicMock): Mock for the datetime module, wrapped to preserve original
            functionality while allowing time override

        Assertions:
            Verifies that returned temperature is equal to 5/8 of hi_temp + (lo_temp - lo_temp),
            meaning user_time, sunset, and night_twilight incremented
        """
        # Arrange: Configure mock responses with valid data and current time
        edge_times = self.sun_times.copy()
        edge_times["morning_twilight"] = time(9, 30)  # 9:30 AM
        edge_times["sunrise"] = time(11, 30)  # 11:30 AM
        edge_times["sunset"] = time(00, 30)  # 12:30 AM
        edge_times["night_twilight"] = time(1, 30)  # 1:30 AM
        mock_get_sun_times.return_value = edge_times

        # Test at 12:45 AM
        test_time = datetime.combine(self.test_date, time(0, 45), tzinfo=timezone.utc)
        mock_datetime.now.return_value = test_time

        # Act
        result = calculate_temp(0, 0)

        # Assert: Calculate expected temperature at 12:45 AM, we're 75 minutes into a 120-minute
        # twilight period, so we're 5/8 through the transition from high to low temp
        twilight_progress = 5 / 8
        expected_temp = self.hi_temp - (self.hi_temp - self.lo_temp) * (
            twilight_progress
        )
        self.assertAlmostEqual(result, expected_temp, places=1)


if __name__ == "__main__":
    unittest.main()
