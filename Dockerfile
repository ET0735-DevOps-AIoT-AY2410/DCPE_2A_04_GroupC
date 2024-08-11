# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

ENV SPI_PATH /app/SPI_Py
WORKDIR /app

# Copy the main.py and the HAL folder
COPY src/main.py ./
COPY src/hal/ ./hal/

# Copy the SPI driver for the RFID Reader
COPY SPI-Py/ /app/SPI_Py/

# Copy the requirements and install them
COPY requirements.txt .

# Install the required libraries 
RUN pip3 install -r requirements.txt
RUN pip3 install spidev
RUN pip3 install --no-cache-dir smbus

# Navigate to the SPI directory and install it
WORKDIR $SPI_PATH
RUN python3 setup.py install

# Trigger Python Script
WORKDIR /app
CMD ["python3", "main.py"]
