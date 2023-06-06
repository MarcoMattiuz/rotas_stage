import asyncio
import json
import websockets.server
from serial import Serial
from base64 import b64encode
import depthai as dai
from time import perf_counter
import cv2

oak = True

# # # # # # # # VIDEO CAM # # # # # # # #
# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)
xoutVideo.setStreamName("video")

# Properties
camRgb.setPreviewSize(640, 480)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.video.link(xoutVideo.input)

#checks if camera is connected
try:
    device = dai.Device(pipeline) 
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)
except:
    print("camera is not connected")
    oak = False

#resize the resolution of the camera
def resize_percent(scale_percent, src):

    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    dsize = (width, height)

    output = cv2.resize(src, dsize)
    return output

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

async def cameraBroadcast():
    while True:
        connections = list(server.websockets)
        if oak and connections:
            inDisparity = q.get() 
            frame = inDisparity.getCvFrame()
            frame = resize_percent(50, frame)
            imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
            imgBASE64 = b64encode(imgJPG_encoded)
            imgBASE64_string = imgBASE64.decode('utf-8')
            for index in range(len(connections)):
                try:
                    await connections[index].send(json.dumps({'img':imgBASE64_string}))
                except websockets.exceptions.ConnectionClosedOK:
                    pass
            await asyncio.sleep(0.01)
        else:
            await asyncio.sleep(1)

#run websocket function
async def main():
    global server
    server = await websockets.server.serve(on_message, '0.0.0.0', 8000)
    asyncio.create_task(sendESPData())
    asyncio.create_task(cameraBroadcast())
    print("Ws started")
    await asyncio.Future() # Run forever
    server.close()

# Start the server
asyncio.run(main())
