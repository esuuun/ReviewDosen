# Use the official Python image from the Docker Hub for Python 3.12.3
FROM python:3.12.3-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Start Gunicorn server
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
