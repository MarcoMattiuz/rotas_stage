import ujson
from config import *
import uasyncio
from uos import dupterm
from utime import sleep

# Disable micropython REPL
# dupterm(None)

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
        
        # print("Awaiting serial data...")
        data = await get_data()
        
        # print("Raw data:", data)
        
        d = '}'

        for toco in data.split(d):
            if toco:
                toco += d
                
                # print("Req:", toco)

                # parse json
                try:
                    doc = ujson.loads(toco)
                except:
                    continue
                
                parsePayload(doc)

def parsePayload(doc: dict):
    response = dict()
    
    if 'left' in doc.keys():
        left = doc['left']

        if left is None:
            response['left'] = leftMotor.power()
        else:
            uasyncio.create_task(leftMotor.asyncPower(int(left)))
            
    if 'right' in doc.keys():
        right = doc['right']

        if right is None:
            response['right'] = rightMotor.power()
        else:
            uasyncio.create_task(rightMotor.asyncPower(int(right)))

    if 'steer' in doc.keys():
        steer = doc['steer']

        try:
            power = doc['accel']
        except KeyError:
            power = 0

        uasyncio.create_task(motors.steerPower(steer, power))

    # if 'oled' in doc.keys():
    #     display.fill(0)
    #     display.text(doc['oled'], 0, 0, 1)
    #     display.show()

    if response:
        print("Res:", response)
        ser.write(ujson.dumps(response).encode())

async def update_coro():
    while True:
        # Update all folks
        gps.get()
        batt.updateLed()

        # Build response json
        response = {
            "batt": {
                "level": batt.lvl,
                "volts": batt.volts
            },
            "gps": {
                "latitude": gps.latitude,
                "longitude": gps.longitude,
                "satellites": gps.satellites
            }
        }

        # Here we could write some data to the OLED
        # display.updateOLED(data)

        # Send data over serial
        print(response)
        ser.write(ujson.dumps(response).encode())
        await uasyncio.sleep_ms(BROADCAST_RATE)

async def main():
    uasyncio.create_task(mainloop())
    uasyncio.create_task(update_coro())
    print("Started")
    while 1:
        await uasyncio.sleep_ms(10_000)

uasyncio.run(main())