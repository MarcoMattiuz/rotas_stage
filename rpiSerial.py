import serial
import json
from time import sleep

ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=.1)

def get_data() -> str:
    data = None
    while data == None:
        try:
            data = ser.readline().decode()
        except AttributeError:
            sleep(0.1)
    return data

while True:
    print(get_data())

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