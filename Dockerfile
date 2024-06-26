# Use the official Python image from the Docker Hub for Python 3.12.3
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Gunicorn server
CMD ["gunicorn", "ReviewDosen.wsgi:application", "--bind", "0.0.0.0:8000"]
