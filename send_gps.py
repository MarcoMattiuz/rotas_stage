import asyncio
import json
import websockets
import random

async def generate_gps_position():
    latitude = random.uniform(10, 20)
    longitude = random.uniform(10, 20)
    pos = {
        'latitude': latitude,
        'longitude': longitude
    }
    json_pos = json.dumps(pos)
    return json_pos

async def send_gps_positions(websocket, path):
    while True:
        gps_position = await generate_gps_position()
        await websocket.send(gps_position)

async def main(websocket):
    async for message in websocket:
        print("Received message:", message)

start_server = websockets.serve(main, "192.168.9.193", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
