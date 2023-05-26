import asyncio
import json
import websockets

#message to send
def on_message(message):

    data = json.loads(message)
    print("triggerR:"+str(data["triggerR"]))
    print("triggerL:"+str(data["triggerL"]))
    print("buttonR:"+str(data["buttonR"]))
    print("buttonL:"+str(data["buttonL"]))
    print("axesXR:"+str(data["axesXR"]))
    print("axesYR:"+str(data["axesYR"]))
    print("axesXL:"+str(data["axesXL"]))
    print("axesYL:"+str(data["axesYL"]))
    print()

#websocket function
async def send_receive(websocket):
    try:
        # receive and send the packets
        async for message in websocket:
            print()
            on_message(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connessione chiusa")


async def main():
    async with websockets.serve(send_receive, "192.168.9.193", 8000):
        print("Server avviato")
        await asyncio.Future() # run forever

asyncio.run(main())
