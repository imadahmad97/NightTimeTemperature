"""Main Application Entry Point

This module serves as the entry point for running the Flask application.
It creates an instance of the application using the factory function and
runs it in debug mode on a specified port.

Usage:
    To run the development server:
        python run.py

Dependencies:
    - app module (containing the create_app factory method)
"""

from app import create_app

# Create an instance of the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application only if this script is executed directly
    app.run(debug=True, port=8080)
