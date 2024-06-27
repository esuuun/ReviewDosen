# Use the official Python image from the Docker Hub for Python 3.12.3
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run migrations, collect static files, and start the server on port 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 ReviewDosen.wsgi"]
