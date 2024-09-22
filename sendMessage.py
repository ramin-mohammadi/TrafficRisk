# Author: Seth Klupka (dyw246)
# Code to write a message to Serial port for transmitter to catch.
# Executed via Raspberry Pi. Simple test code to adapted elsewhere.

import serial
from time import sleep

# Depends on what port # is used for transmitter (ESP32).
# List ports: `ls -l /dev/t*`
# list usb buses and what is c onnected in those buses: `ls -R /dev/bus/usb`
# Port # can change even when using the same physical port on Raspberry Pi.
ser = serial.Serial("/dev/ttyUSB0", 115200) 

# Write message data here. To see if new message is being sent,
# change the message and try again.
message = "Hello, Wodrld!ddd"

# Write message to Serial port.
ser.write(message.encode())


# Temp
# Humidity
# Light (empty for now)
# Speed
# Traffic Vol