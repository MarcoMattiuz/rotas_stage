import asyncio
import json
import websockets.server
from serial import Serial
import random
from time import perf_counter

ser = Serial(port='/dev/ttyS0', baudrate=115200, timeout=.1)

# WebSocket message receive and send
async def on_message(websocket):
    global serial_available, gps_requested, batt_requested

    async for message in websocket:
        msg = json.loads(message)

        print(msg, websocket)

        # Send data to ESP32
        ser.write(message.encode())

        if 'left' in msg.keys():
            print("left:", msg["left"])
        
        if 'right' in msg.keys():
            print("right:", msg["right"])

        if 'gps' in msg.keys():
            gps_requested = websocket
            # print("gps requested")

        if 'batt' in msg.keys():
            batt_requested = websocket
            # print("batt requested")

        # if 'msg' in msg.keys():
        #     print("Ip connceted:", msg["msg"])
        
async def getESPData(blocking = True):
    data = ""
    cont = True
    while data == "" and cont:
        try:
            data = ser.readline().decode()
        except AttributeError:
            await asyncio.sleep(.1)
        cont = blocking
    return data

async def sendESPData():
    global gps_requested, batt_requested, server

    data = ''

    while True:
        await asyncio.sleep(.1)

        if not server.websockets:
            continue

        if gps_requested and batt_requested:
            data = await getESPData(False)
            if data:
                print(data)
                try:
                    await gps_requested.send(data)
                except websockets.exceptions.ConnectionClosedOK:
                    pass
                try:
                    await batt_requested.send(data)
                except websockets.exceptions.ConnectionClosedOK:
                    pass
                gps_requested = False
                batt_requested = False
            
        elif batt_requested:
            data = await getESPData(False)
            if data:
                print(data)
                await batt_requested.send(data)
                batt_requested = False
        
        elif gps_requested:
            data = await getESPData(False)
            if data:
                print(data)
                try:
                    await gps_requested.send(data)
                except websockets.exceptions.ConnectionClosedOK:
                    pass
                gps_requested = False

async def checkSerial(event: asyncio.Event, wait_for_flush = False):
    while True:
        if ser.in_waiting:
            await event.set()

            # Ensure fresh data
            timeout = await perf_counter() + SERIAL_TIMEOUT

            # Wait for the buffer to flush
            while ser.in_waiting and timeout > await perf_counter() and wait_for_flush:
                await asyncio.sleep(.1)
            
            await event.clear()
            
            if wait_for_flush: await ser.reset_input_buffer()
        else:
            await asyncio.sleep(.1)

SERIAL_TIMEOUT = 10

serial_available = asyncio.Event()

server = None

gps_requested = False
batt_requested = False

current_websocket = None

#run websocket function
async def main():
    global server
    server = await websockets.server.serve(on_message, '0.0.0.0', 8000)
    asyncio.create_task(sendESPData())
    print("Ws started")
    await asyncio.Future() # Run forever
    server.close()

# Start the server
asyncio.run(main())
