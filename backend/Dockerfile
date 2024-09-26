# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.12-slim
# Install system dependencies for building cvxopt and other Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt, including cvxopt (from source)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that FastAPI will be running on
EXPOSE 8000

# Command to run FastAPI server (adjust if needed)
CMD ["uvicorn", "api_calls:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
