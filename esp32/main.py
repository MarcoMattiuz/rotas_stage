from time import sleep
import ujson
import uasyncio
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
    
    response = False

    # parse json
    doc = ujson.loads(data)

    # check if any data is requested
    if 'batt' in doc.keys():
        battdata = {
            "level": batt.level(),
            "volts": batt.voltage()
        }

    if 'gps' in doc.keys():
        gps.get()
        gpsdata = {
            "latitude": gps.latitude,
            "longitude": gps.longitude,
            "satellites": gps.satellites
        }
    
    if 'left' in doc.keys():
        left = doc['left']
        if left is None:
            leftdata = 

    left = int(doc["left"])
    right = int(doc["right"])
    oled = doc["oled"]
    
    # activate motors/display
    leftMotor.power(left)
    rightMotor.power(right)

    display.fill(0)
    display.text(oled, 0, 0, 1)
    display.show()

    # return data
    if response:
        ser.write(ujson.dumps({
            "gps": gpsdata,
            "batt": battdata
        }).encode())


while True:
    mainloop()