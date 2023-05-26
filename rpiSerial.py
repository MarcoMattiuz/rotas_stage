import serial
import json
from time import sleep

ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=.1)

while True:
    right = int(input("right: "))
    left = int(input("left: "))
    oled = (input("oled: "))
    
    jsonData = {
        "left": left,
        "right": right,
        "oled": oled
    }

    payload = json.dumps(jsonData).encode()
    ser.write(payload)