import serial
import json
from time import sleep

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)


def func():
    data = ''
    while data == '':
        ser.write(payload)
        data = str(ser.readline(), encoding='utf-8')
    while ser.in_waiting: data += str(ser.readline(), 'utf-8')

    print("\n")

while True:
    right = int(input(":"))
    left = int(input(":"))
    
    if right == 0 and left == 0:
        break
    
    if right != 0 and left != 0:
        jsonData = {
        "right": right,
        "left": left
        }

        payload = json.dumps(jsonData).encode()
        func()

ser.close()
