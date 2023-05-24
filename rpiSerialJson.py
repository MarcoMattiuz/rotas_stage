import serial
import json
from time import sleep

ser = serial.Serial(port='/dev/ttyACM1', baudrate=9600, timeout=.1)

jsonData = {
    "right": 10,
    "left": 10
}

payload = json.dumps(jsonData).encode()

def func():
    data = ''
    while data == '':
        ser.write(payload)
        data = str(ser.readline(), encoding='utf-8')
    while ser.in_waiting: data += str(ser.readline(), 'utf-8')

    print("Ricevuto: ", end='')
    print(data)

while input("-->") != "exit": func()


ser.close()
