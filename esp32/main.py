import ujson
from config import *
import uasyncio
from uos import dupterm
from utime import sleep

dupterm(None)

async def get_data(blocking = True) -> str:
    data = None
    while data == None and blocking:
        try:
            data = ser.readline().decode()
        except AttributeError:
            await uasyncio.sleep_ms(100)
    return data

async def mainloop():
    
    while True:
        # get data from serial
        
        data = await get_data()

        
        d = '}'

        for toco in data.split(d):
            if toco:
                toco += d
                
                
                # parse json
                try:
                    doc = ujson.loads(toco)
                except:
                    
                    continue
                
                parsePayload(doc)

def parsePayload(doc: dict):
    response = dict()

    # check if any data is requested
    if 'batt' in doc.keys():
        response['batt'] = {
            "level": batt.level(),
            "volts": batt.voltage()
        }

    if 'gps' in doc.keys():
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

    # if 'oled' in doc.keys():
    #     display.fill(0)
    #     display.text(doc['oled'], 0, 0, 1)
    #     display.show()

    if response:
        
        ser.write(ujson.dumps(response).encode())

async def gps_coro():
    while True:
        gps.get()
        await uasyncio.sleep_ms(100)

async def main():
    uasyncio.create_task(mainloop())
    uasyncio.create_task(gps_coro())
    
    while 1:
        await uasyncio.sleep_ms(10_000)

uasyncio.run(main())