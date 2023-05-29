from utime import sleep
import ujson
from config import *

def get_data() -> str:
    data = None
    while data == None:
        try:
            data = ser.readline().decode()
        except AttributeError:
            sleep(0.1)
    return data

def mainloop():
    # get data from serial
    data = get_data()
    
    response = dict()

    # parse json
    doc = ujson.loads(data)

    # check if any data is requested
    if 'batt' in doc.keys():
        response['batt'] = {
            "level": batt.level(),
            "volts": batt.voltage()
        }

    if 'gps' in doc.keys():
        gps.get()
        response['gps'] = {
            "latitude": gps.latitude,
            "longitude": gps.longitude,
            "satellites": gps.satellites
        }
    
    if 'left' in doc.keys():
        left = doc['left']

        if left is None:
            response['left'] = leftMotor.power()
        else:
            leftMotor.power(int(left))
            
    if 'right' in doc.keys():
        right = doc['right']

        if right is None:
            response['right'] = rightMotor.power()
        else:
            rightMotor.power(int(right))

    if 'oled' in doc.keys():
        display.fill(0)
        display.text(doc['oled'], 0, 0, 1)
        display.show()

    # return data
    if response:
        ser.write(ujson.dumps(response).encode())


while True:
    mainloop()