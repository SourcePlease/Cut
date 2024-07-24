# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Make port 8443 available to the world outside this container
EXPOSE 8443

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
