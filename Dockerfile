# Use an official Python 3.12 Alpine image as the base image
FROM python:3.12-alpine

# Install system dependencies
RUN apk --update add --virtual build-dependencies \
    python3-dev \
    libffi-dev \
    openssl-dev \
    build-base \
    postgresql-dev \
    && apk add postgresql-client  # Add PostgreSQL client

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Create and activate a virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN /app/venv/bin/pip install --upgrade pip

# Install project dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the container
COPY entrypoint.sh .

# Set permissions for the entrypoint script
RUN chmod +x entrypoint.sh

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on (adjust as needed)
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0  # Set DEBUG to 0 for production

# Start the application using the entrypoint script
CMD ["./entrypoint.sh"]
