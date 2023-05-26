import asyncio
import json
import websockets

import random
def generate_gps_position():
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return {"latitude": latitude, "longitude": longitude}


# WebSocket message receive and send
async def on_message(websocket):
    async for message in websocket:
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

        
        await websocket.send(generate_gps_position)

#run websocket function
async def main():
    async with websockets.serve(on_message, "192.168.9.193", 8000):
        print("Server avviato")
        await asyncio.Future() # Run forever

# Start the server
asyncio.run(main())
