# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3
ENV SPI_PATH /app/SPI_Py
WORKDIR /app

# Copy the main.py and the HAL folder
COPY src/main.py ./
COPY hal ./hal

# Copy the SPI driver for the RFID Reader
COPY SPI-Py ./SPI-Py

# Install the required libraries 
RUN pip3 install --no-cached-dir -r requirements.txt
RUN pip3 install --no-cached-dir spidev

WORKDIR $SPI_PATH
RUN python3 setup.py install

# Trigger Python Script
WORKDIR /app
CMD ["python3", "src/main.py"]