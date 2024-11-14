# Dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run tests and fail the build if any tests fail
RUN python -m unittest discover app/tests || exit 1

# Default environment variables 
ENV FLASK_APP=run.py

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
