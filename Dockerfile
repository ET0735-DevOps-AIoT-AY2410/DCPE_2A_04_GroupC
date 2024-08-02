# Use the official Python image from the Docker Hub
FROM balenalib/rpi-raspbian:bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app/src

# Install any required packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define the command to run your application
CMD ["python", "src/main_menu.py"]