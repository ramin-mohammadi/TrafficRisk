# Author: Seth Klupka (dyw246)
# Loop through display modes, Temp, Humidity, Light, Speed, Traffic Volume 
# API Reference: https://pythonhosted.org/sense-hat/api/

import os
import time
from sense_hat import SenseHat
import board
import busio
import adafruit_tsl2591

# --- Sending Message, Receiver to Transmitter --- #
import serial
from time import sleep

# Depends on what port # is used for transmitter (ESP32).
# List ports: `ls -l /dev/t*`
# list usb buses and what is connected in those buses: `ls -R /dev/bus/usb`

# MAKE SURE transmitter is plugged into bottom right usb and use /dev/ttyUSB0
ser = serial.Serial("/dev/ttyUSB0", 115200)

# ------------------------------------------------- #

# --- Light Sensor -------------
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)
#-------------------------------

sense = SenseHat()

# Delete existing file
if(os.path.exists("data.txt")):
    os.remove("data.txt")

# Function to convert celsius to fahrenheit (if needed)
def tofahrenheit(celsius):
    return( (celsius*(9/5))+32 )

# Create new file
if not(os.path.exists("data.txt")):
    f = open("data.txt", "w")
    column_names = ['Humidity(%rH)','Pressure(mb)','Temperature(C)','DP_Class','Temp_Class']
    col_sep_names = ','.join(column_names)
    f.write(col_sep_names + "\n")
    f.close()
    print("New file created.\n")
    print("Line\t", column_names)

# Get dew point using temp(C) and %rH
def get_dp_class():
    # Get sensor data
    temp = sense.get_temperature()
    rh = sense.get_humidity()
    
    # Dew point formula
    dew_point = temp - ((100 - rh)/5)
    
    # Dew point classification.
    # Source: https://www.weather.gov/arx/why_dewpoint_vs_humidity
    if dew_point <= 55:
        return "DRY"
    elif 55 < dew_point < 65:
        return "STICKY"
    elif dew_point >= 65:
        return "WET"

def get_temp_class():
    # Get sensor data
    temp = sense.get_temperature()
    
    # Temperature classification.
    # Source: https://thinkmetric.uk/basics/temperature/
    if temp <= 0:
        return "FREEZING"
    elif 0 < temp <= 10:
        return "COLD"
    elif 10 < temp <= 20:
        return "COOL"
    elif 20 < temp < 30:
        return "WARM"
    elif 30 < temp <= 35:
        return "HOT"
    elif temp > 35:
        return "VERY HOT"
    
i = 0
while True:
    
    # call classification functions to get dp and temp class
    dp_class = get_dp_class()
    temp_class = get_temp_class()
    
    # get raw data for each if
    if (i == 0):
        humidity = float("{:.1f}".format(sense.get_humidity()))
        message = str(humidity) + "  " + str(dp_class)
        print(message)
        i = i+1
    elif (i==1):
        temp_as_f = tofahrenheit(sense.get_temperature())
        temperature = float("{:.1f}".format(temp_as_f))
        temp_string = str(temperature) + " " + str(temp_class)
        message = temp_string
        print(message)
        i = i+1
    elif (i==2):
        message = "ex. speed"
        print(message)
        i = 0
    
    #ser.write(message.encode())

    #print(i, "\t", data_row)
    print("\n")
    
    # ----- Light Sensor -------
    # Read and calculate the light level in lux.
    lux = sensor.lux
    print("Total light: {0}lux".format(lux))
    # You can also read the raw infrared and visible light levels.
    # These are unsigned, the higher the number the more light of that type.
    # There are no units like lux.
    # Infrared levels range from 0-65535 (16-bit)
    infrared = sensor.infrared
    print("Infrared light: {0}".format(infrared))
    # Visible-only levels range from 0-2147483647 (32-bit)
    visible = sensor.visible
    print("Visible light: {0}".format(visible))
    # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
    full_spectrum = sensor.full_spectrum
    print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
    #--------------------------
    
    # ---- Send message to receiver ---- #
    send_mess = ""
    # Humidity
    send_mess += "H: " + str(humidity) + "\n"
    # Light (lux value)
    send_mess += "L: {0}\n".format(round(lux,2))
    # Risk prediction
    send_mess += "minor" # manually change to Low, Medium, High for now
    #send_mess = dp_class + "\n" + temp_class
    # Write message to Serial port.
    ser.write(send_mess.encode())
    #------------------------------------#
    time.sleep(3)
    
    

