import asyncio
import json
import websockets
from serial import Serial
import random

ser = Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=.1)

def generate_gps_position():
    latitude = random.uniform(10, 20)
    longitude = random.uniform(10, 20)
    pos = {
        'latitude': latitude,
        'longitude': longitude
    }
    json_pos = json.dumps(pos)
    return json_pos

def getEspData():
    raise NotImplementedError("Mona")

# WebSocket message receive
async def on_message(websocket):
    while True:
        message = await websocket.recv()
        if message:
            data = json.loads(message)
            print("triggerR:", data["triggerR"])
            print("triggerL:", data["triggerL"])
            print("buttonR:", data["buttonR"])
            print("buttonL:", data["buttonL"])
            print("axesXR:", data["axesXR"])
            print("axesYR:", data["axesYR"])
            print("axesXL:", data["axesXL"])
            print("axesYL:", data["axesYL"])
            print()

#run websocket function
async def main():
    async with websockets.serve(on_message, "192.168.9.193", 8000):
        print("Server avviato")
        await asyncio.Future() # Run forever

        
# Start the server
asyncio.run(main())