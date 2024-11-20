"""
Configuration and Application Factory Test Module.

This module contains unit tests for the configuration classes, the get_config function, and the
Flask application factory. It verifies the correct behavior of different configuration settings and
ensures that the application is properly initialized with the appropriate configuration.

Test Coverage:
    - Base, Development, and Production configuration settings
    - Environment-based configuration selection
    - Flask application factory initialization

Dependencies:
    unittest: Standard Python testing framework
    unittest.mock: For mocking environment variables and functions
    os: For environment variable manipulation
    flask: Web framework for the application
    app.config: Custom configuration classes and functions
    app: Application factory module
"""

import unittest
from unittest.mock import patch
import os
from flask import Flask
from app.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    get_config,
)
from app import (
    create_app,
)


class TestConfig(unittest.TestCase):
    """
    Unit test suite for configuration classes and the get_config function.

    This class contains test cases to verify the correct settings of different configuration classes
    and the behavior of the get_config function under various environment settings.

    Test Methods:
        test_base_config: Verifies the settings of the base Config class.
        test_development_config: Checks the settings of the DevelopmentConfig class.
        test_production_config: Ensures correct settings for the ProductionConfig class.
        test_get_config_dev: Tests get_config function with 'dev' profile.
        test_get_config_pr: Tests get_config function with 'pr' profile.
    """

    def test_base_config(self):
        """Test the base Config class settings.

        Args:
            self: The test case instance.

        Assertions:
            - DEBUG is False
            - MOCK_VALUES is False
        """
        # Arrange and Act: Load the Config class from Config
        config = Config()

        # Assert: Verify DEBUG and MOCK_VALUES are False
        self.assertFalse(config.DEBUG)
        self.assertFalse(config.MOCK_VALUES)

    def test_development_config(self):
        """Test the DevelopmentConfig class settings.

        Args:
            self: The test case instance.

        Assertions:
            - DEBUG is True
            - MOCK_VALUES is True
        """
        # Arrange and Act: Load the DevelopmentConfig class from Config
        config = DevelopmentConfig()

        # Assert: Verify DEBUG and MOCK_VALUES are True
        self.assertTrue(config.DEBUG)
        self.assertTrue(config.MOCK_VALUES)

    def test_production_config(self):
        """Test the ProductionConfig settings.

        Args:
            self: The test case instance.

        Assertions:
            - DEBUG is False
            - MOCK_VALUES is False
        """
        # Arrange and Act: Load the ProductionConfig class from Config
        config = ProductionConfig()

        # Assert: Verify DEBUG and MOCK_VALUES are False
        self.assertFalse(config.DEBUG)
        self.assertFalse(config.MOCK_VALUES)

    @patch.dict(os.environ, {"PROFILE": "dev"})
    def test_get_config_dev(self):
        """Test get_config returns DevelopmentConfig when PROFILE is 'dev'.

        Args:
            self: The test case instance.

        Assertions:
            - The config class is set to DevelopmentConfig.
        """
        # Arrange and Act: Get the config when env var set to dev
        config_class = get_config()

        # Assert: Verify the DevelopmentConfig class is returned
        self.assertEqual(config_class, DevelopmentConfig)

    @patch.dict(os.environ, {"PROFILE": "pr"})
    def test_get_config_pr(self):
        """Test get_config returns ProductionConfig when PROFILE is 'pr'.

        Args:
            self: The test case instance.

        Assertions:
            - The config class is set to ProductionConfig.
        """
        # Arrange and Act: Get the config when env var set to pr
        config_class = get_config()

        # Assert: Verify the ProductionConfig class is returned
        self.assertEqual(config_class, ProductionConfig)


class TestAppFactory(unittest.TestCase):
    """
    Unit test suite for the Flask application factory.

    This class contains test cases to verify that the create_app function correctly initializes a
    Flask application with the appropriate configuration based on the environment.

    Test Methods:
        test_create_app_with_development_config: Tests app creation with DevelopmentConfig.
        test_create_app_with_production_config: Tests app creation with ProductionConfig.
    """

    @patch("app.get_config", return_value=DevelopmentConfig)
    def test_create_app_with_development_config(self, mock_get_config):
        """Test create_app initializes app with DevelopmentConfig.

        Args:
            mock_get_config: Mocked get_config function.

        Assertions:
            - Returned object is a Flask instance
            - DEBUG is True
            - MOCK_VALUES is True
        """
        # Arrange and Act: Create an app with config set to DevelopmentConfig
        app = create_app()

        # Assert that Flask instance is returned with DEBUG and MOCK_VALUES set to True
        self.assertIsInstance(app, Flask)
        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(app.config["MOCK_VALUES"])

    @patch("app.get_config", return_value=ProductionConfig)
    def test_create_app_with_production_config(self, mock_get_config):
        """Test create_app initializes app with ProductionConfig.

        Args:
            mock_get_config: Mocked get_config function.

        Assertions:
            - Returned object is a Flask instance
            - DEBUG is False
            - MOCK_VALUES is False
        """
        # Arrange and Act: Create an app with config set to ProductionConfig
        app = create_app()

        # Assert that Flask instance is returned with DEBUG and MOCK_VALUES set to False
        self.assertIsInstance(app, Flask)
        self.assertFalse(app.config["DEBUG"])
        self.assertFalse(app.config["MOCK_VALUES"])


if __name__ == "__main__":
    unittest.main()
