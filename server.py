import asyncio
import json
import websockets
from serial import Serial
import random
from time import sleep

ser = Serial(port='/dev/ttyS0', baudrate=115200, timeout=.1)

def getEspData(req: str):
    ser.write(req.encode())
    data = ""
    while data == "":
        try:
            data = ser.readline().decode()
        except AttributeError:
            sleep(0.01)
    return data

# WebSocket message receive and send
async def on_message(websocket):
    data_prec=""
    data=""
    async for message in websocket:
        msg = json.loads(message)

        if 'left' in msg.keys() and 'right' in msg.keys():
            print("left:", msg["left"])
            print("right:", msg["right"])
        
        if 'gps' in msg.keys() and 'batt' in msg.keys():
            # print("gps required")
            # print("batt required")
            data=getEspData(message)
            # print("--- ESP DATA ---")

            # print(data, '')
            await websocket.send(data)

#run websocket function
async def main():
    async with websockets.serve(on_message, "192.168.9.193", 8000):
        print("Server avviato")
        await asyncio.Future() # Run forever

# Start the server
asyncio.run(main())
