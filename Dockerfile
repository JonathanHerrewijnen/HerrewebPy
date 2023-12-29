# Use an official Python runtime as a parent image
FROM python:3.9-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Intermediate build stage (named 'dev' for example)
FROM base AS dev

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
