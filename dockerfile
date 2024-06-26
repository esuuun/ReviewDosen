# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run the migration and start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn ReviewDosen.wsgi:application --bind 0.0.0.0:8000"]
