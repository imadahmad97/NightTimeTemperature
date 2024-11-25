# from unittest.mock import patch, MagicMock
# from flask import jsonify, Flask
# from app import main
# import unittest
# from datetime import datetime, timezone
# from app.sun_times import SunTimes


# class TestMain(unittest.TestCase):
#     def setUp(self):
#         # Initialize the Flask app and push the app context
#         self.app = Flask(__name__)
#         self.app.config["HI_TEMP"] = 6000
#         self.app.config["LO_TEMP"] = 2700
#         self.app.config["SUNRISE_SUNSET_API_BASE_URL"] = (
#             "https://api.sunrise-sunset.org/json?"
#         )
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         self.client = self.app.test_client()

#     def tearDown(self):
#         # Remove the app context after each test
#         self.app_context.pop()

#     # def test_main_with_mocked_fetch_sun_times(self):
#     #     # Mock data to return from fetch_sun_times
#     #     mock_json_data = {
#     #         "results": {
#     #             "sunrise": "6:00:00 AM",
#     #             "sunset": "6:00:00 PM",
#     #             "civil_twilight_begin": "5:00:00 AM",
#     #             "civil_twilight_end": "6:30:00 PM",
#     #         },
#     #         "status": "OK",
#     #         "tzid": "UTC",
#     #     }

#     #     # Create a mock `Response` object
#     #     mock_response = MagicMock()
#     #     mock_response.status_code = 200  # Simulate HTTP 200 status
#     #     mock_response.json.return_value = mock_json_data

#     #     # Patch SunTimesAPI.fetch_sun_times to return mock_response
#     #     with patch(
#     #         "app.process_response.process_response_utils.sun_times_api.SunTimesAPI.fetch_sun_times",
#     #         return_value=mock_response,
#     #     ):
#     #         # Call the main function
#     #         response = main.main()

#     #         # Assert the result
#     #         # You might need to adjust the expected response based on your actual implementation
#     #         expected_temperature = (
#     #             2700  # Assuming CalculateTemp.calculate_temp computes this
#     #         )
#     #         expected_response = jsonify(temperature=expected_temperature)

#     #         # Validate the JSON response and status code
#     #         assert response.get_json() == expected_response.get_json()
#     #         assert response.status_code == 200

#     @patch(
#         "app.process_response.process_response_utils.sun_times_api.SunTimesAPI.fetch_sun_times"
#     )
#     @patch("app.sun_times.datetime.datetime")
#     def test_user_in_midday(self, mock_datetime_module, mock_fetch_sun_times):
#         # Mock datetime.datetime.now to return a specific user_time
#         mock_datetime = mock_datetime_module.datetime
#         mock_datetime.now.return_value = datetime(
#             2024, 1, 1, 7, 30, 0, tzinfo=timezone.utc
#         )

#         # Create a mock Response object
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             "results": {
#                 "sunrise": "06:00:00 AM",
#                 "sunset": "06:00:00 PM",
#                 "solar_noon": "12:00:00 PM",
#                 "day_length": "12:00:00",
#                 "civil_twilight_begin": "05:00:00 AM",
#                 "civil_twilight_end": "06:30:00 PM",
#                 "nautical_twilight_begin": "04:30:00 AM",
#                 "nautical_twilight_end": "07:00:00 PM",
#                 "astronomical_twilight_begin": "04:00:00 AM",
#                 "astronomical_twilight_end": "07:30:00 PM",
#             },
#             "status": "OK",
#             "tzid": "UTC",
#         }

#         # Mock fetch_sun_times to return the mock Response object
#         mock_fetch_sun_times.return_value = mock_response

#         # Create a test request context
#         with self.app.test_request_context("/?lat=49.2827&lng=-123.1207", method="GET"):
#             # Call the main function
#             response = main.main()

#             # Define expected temperature
#             expected_temperature = (
#                 6000  # Assuming CalculateTemp.calculate_temp computes this
#             )

#             # Validate the JSON response and status code
#             self.assertEqual(response.get_json(), {"temperature": expected_temperature})
#             self.assertEqual(response.status_code, 200)

#             # Ensure fetch_sun_times was called once
#             mock_fetch_sun_times.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()
