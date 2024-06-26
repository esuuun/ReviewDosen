# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS dependencies for our mini VM
RUN apt-get update && apt-get install -y \
    # For PostgreSQL
    libpq-dev \
    # For Pillow
    libjpeg-dev \
    # For CairoSVG
    libcairo2 \
    # Other tools
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python project requirements
RUN . /opt/venv/bin/activate && \
    pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Set the Django default project name
ARG PROJ_NAME="ReviewDosen"

# Create a bash script to run the Django project
RUN printf "#!/bin/bash\n" > ./docker-entrypoint.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./docker-entrypoint.sh && \
    printf "python manage.py migrate --no-input\n" >> ./docker-entrypoint.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./docker-entrypoint.sh

# Make the bash script executable
RUN chmod +x docker-entrypoint.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the entrypoint script
CMD ["./docker-entrypoint.sh"]
