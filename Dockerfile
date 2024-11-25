# Dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run tests and fail the build if any tests fail
RUN python -m unittest discover app || exit 1

# Set environment variable for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose the application port
EXPOSE 8080

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
