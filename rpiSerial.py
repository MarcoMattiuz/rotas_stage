import serial
import json
from time import sleep

ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, timeout=.1)

def get_data() -> str:
    data = ""
    while data == "":
        try:
            data = ser.readline().decode()
        except AttributeError:
            sleep(0.1)
    return data

while True:
    # right = int(input("right: "))
    # left = int(input("left: "))
    # oled = (input("oled: "))
    
    jsonData = {
        "left": None,
        "right": None,
        "gps": None,
        "batt": None
    }

    payload = json.dumps(jsonData).encode()
    ser.write(payload)

    recv = get_data()
    print(recv)