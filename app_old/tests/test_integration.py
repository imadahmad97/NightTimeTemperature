"""Integration Test Module for Night-Time Temperature API Service.

This module contains integration tests for the Flask-based night-time temperature API service. It
tests the complete request-response cycle of the API endpoint, including input validation, error
handling, and response formatting.

The test suite uses Flask's test client to simulate HTTP requests and verify the API's behavior
across various scenarios, including both valid and invalid inputs.

Test Coverage:
    - Valid coordinate inputs
    - Missing parameters
    - Invalid parameter types
    - Out-of-range coordinates
    - Internal error handling
    - JSON response formatting
    - Edge case coordinate values

Dependencies:
    unittest: Standard Python testing framework
    unittest.mock: For mocking external dependencies
    flask: Web framework for the API
    warnings: For suppressing Flask deprecation warnings
"""

import unittest
from unittest.mock import patch
import warnings
from flask import Flask
from app.routes import (
    register_routes,
)


class TestTemperatureService(unittest.TestCase):
    """
    Unit test suite for the night-time temperature API route.

    This class contains a series of test cases to verify the functionality, error handling, and edge
    cases of the night-time temperature API endpoint.

    Attributes:
        app (Flask): The Flask application instance used for testing.
        client (FlaskClient): The test client used to make requests to the API.

    Test Methods:
        test_route_valid_input:
            Verifies correct response for valid latitude and longitude inputs.

        test_route_missing_parameters:
            Checks error handling when required parameters are missing.

        test_route_invalid_parameter_type:
            Tests response when invalid data types are provided for coordinates.

        test_route_out_of_range_coordinates:
            Verifies error handling for out-of-range latitude and longitude values.

        test_route_internal_error:
            Simulates and tests handling of internal server errors.

        test_route_json_response:
            Ensures that the API returns properly formatted JSON responses.

        test_route_edge_case_coordinates:
            Tests the API's behavior with edge case coordinate values.
    """

    def setUp(self):
        """Set up a Flask test client and mock configuration to run before each test method.

        This method creates a mock configuration with both TESTING and MOCK_VALUES equal to True,
        simulating a test environment."""

        # Hide warning for deprecated werkzeug command (current version of flask still uses this)
        warnings.filterwarnings(
            "ignore", category=DeprecationWarning, module="flask.testing"
        )

        # Initializes app, setting TESTING and MOCK_VALUES to True
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["MOCK_VALUES"] = True
        register_routes(app)
        self.app = app
        self.client = app.test_client()

    def test_route_valid_input(self):
        """Test the endpoint with valid latitude and longitude inputs.

        Args:
            self: The test case instance.

        Assertions:
            - The API route returns a 200 (Success) status code
            - The API route returns the key temperature
            - The mock temperature of 15 is returned
        """
        # Arrange and act: Create mock response
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 40.7128, "lng": -74.0060}
        )

        # Assert: Check that we get back a succesful status code, and temperature of 15
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("temperature", data)
        self.assertEqual(data["temperature"], 15.0)

    def test_route_missing_parameters(self):
        """Test the endpoint with a missing longitude parameter.

        Args:
            self: The test case instance.

        Assertions:
            - The API route returns a 400 (Bad Request) status code
            - The API route returns the key error
        """
        # Arrange and act: Create mock response missing longitude
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 40.7128}
        )

        # Assert: Check that we get a 400 status code and error key in response
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_route_invalid_parameter_type(self):
        """Test the endpoint with invalid data types for latitude and longitude.

        Args:
            self: The test case instance.

        Assertions:
            - The API route returns a 400 (Bad Request) status code
            - The API route returns the key error
        """
        # Arrange and act: Create mock response with invalid (string) latitude and longitude
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": "invalid", "lng": "invalid"}
        )

        # Assert: Check that we get a 400 status code and error key in response
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    def test_route_out_of_range_coordinates(self):
        """Test the endpoint with out-of-range latitude and longitude values.

        Args:
            self: The test case instance.

        Assertions:
            - The API route returns a 400 (Bad Request) status code
            - The API route returns the key error
        """
        # Arrange and act: Create mock response with out of range latitude and longitude
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 100.0, "lng": -200.0}
        )

        # Assert: Check that we get a 400 status code and error key in response
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    @patch("app.routes.calculate_temp")
    def test_route_internal_error(self, mock_calculate_temp):
        """Test the endpoint with an internal error in the calculation function.

        Args:
            self: The test case instance.
            mock_calculate_temp: A mock instance of the calculate_temp function.

        Assertions:
            - The API route returns a 400 (Bad Request) status code
            - The API route returns the key error
        """
        # Arrange: Create a mock error response from calculate_temp
        mock_calculate_temp.side_effect = RuntimeError("Internal Server Error")

        # Act
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 40.7128, "lng": -74.0060}
        )

        # Assert: Check that we get a 400 status code and error key in response
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    def test_route_json_response(self):
        """Test that the response content type is JSON and contains expected keys.

        Args:
            self: The test case instance.

        Assertions:
            - The API returns a JSON
            - The API route returns a 200 (Success) status code
            - The API route returns the temperature key
        """
        # Arrange and act: Create mock API response
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 40.7128, "lng": -74.0060}
        )

        # Assert: Check that we get a 200 status code and temperature key in valid JSON response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        data = response.get_json()
        self.assertIn("temperature", data)

    def test_route_edge_case_coordinates(self):
        """Test the endpoint with edge case values for latitude and longitude.

        Args:
            self: The test case instance.

        Assertions:
            - The API route returns a 200 (Success) status code
            - The API route returns the temperature key
        """
        # Arrange and act: Create mock API response with edge case latitude and longitude
        response = self.client.get(
            "/night-time-temperature", query_string={"lat": 90.0, "lng": 180.0}
        )

        # Assert: Check that we get a 200 status code and temperature key in response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("temperature", data)


if __name__ == "__main__":
    unittest.main()
