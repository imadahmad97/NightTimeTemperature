"""Application Configuration Module.

This module defines configuration classes for different environments
and provides a function to retrieve the appropriate configuration based
on the environment.

Configuration classes:
    Config: Base configuration class with default settings.
    DevelopmentConfig: Configuration for development environment.
    ProductionConfig: Configuration for production environment.

Environment Variables:
    PROFILE: Determines which configuration to use.
             Values: 'dev' (default) for development, 'pr' for production.
"""

import os


class Config:
    """Base configuration class.

    This class contains default configuration settings.
    All environment-specific configurations should inherit from this class.

    Attributes:
        DEBUG (bool): Flag to enable/disable debug mode.
        MOCK_VALUES (bool): Flag to enable/disable use of mock values.
    """

    DEBUG = False
    MOCK_VALUES = False


class DevelopmentConfig(Config):
    """Development environment configuration.

    This class contains configuration settings specific to the
    development environment.

    Attributes:
        DEBUG (bool): Debug mode enabled for development.
        MOCK_VALUES (bool): Mock values enabled for development testing.
    """

    DEBUG = True
    MOCK_VALUES = True


class ProductionConfig(Config):
    """Production environment configuration.

    This class contains configuration settings specific to the
    production environment.

    Attributes:
        DEBUG (bool): Debug mode disabled for production.
        MOCK_VALUES (bool): Mock values disabled for production.
    """

    DEBUG = False
    MOCK_VALUES = False


def get_config():
    """Retrieve the appropriate configuration based on the environment.

    This function checks the 'PROFILE' environment variable to determine
    which configuration to use. If not set or set to 'dev', it returns
    the DevelopmentConfig. If set to 'pr', it returns the ProductionConfig.

    Returns:
        type: Configuration class (either DevelopmentConfig or ProductionConfig)
    """
    # Get the PROFILE environment variable, defaulting to 'dev' if not set
    profile = os.getenv("PROFILE", "dev")

    if profile == "pr":
        return ProductionConfig
    return DevelopmentConfig
