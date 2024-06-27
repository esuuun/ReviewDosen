# Use the official Python image from the Docker Hub for Python 3.12.3
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Collect static files during the build process
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 ReviewDosen.wsgi"]
