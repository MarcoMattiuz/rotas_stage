import asyncio
import json
import websockets.server
from serial import Serial
from base64 import b64encode
import depthai as dai
from time import perf_counter

# WebSocket message receive and send
async def on_message(websocket):
    global serial_available, gps_requested, batt_requested

    async for message in websocket:
        msg = json.loads(message)

        print(msg, websocket)

        if 'left' in msg.keys():
            print("left:", msg["left"])
        
        if 'right' in msg.keys():
            print("right:", msg["right"])

        if 'img' in msg.keys() and not oak:
            await websocket.send(json.dumps({'img': None}))

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

oak = True

async def cameraBroadcast():
    global oak
    # Create pipeline
    pipeline = dai.Pipeline()

    # Define sources and output
    camRgb = pipeline.create(dai.node.ColorCamera)
    videoEnc = pipeline.create(dai.node.VideoEncoder)
    manip = pipeline.create(dai.node.ImageManip)
    xout = pipeline.create(dai.node.XLinkOut)

    xout.setStreamName('raw')

    # Properties
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setPreviewSize(832, 480)
    camRgb.setFps(20)

    manip.initialConfig.setResize(832, 480)
    manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
    manip.setMaxOutputFrameSize(2000000)

    videoEnc.setDefaultProfilePreset(20, dai.VideoEncoderProperties.Profile.MJPEG)
    # videoEnc.setBitrateKbps(100)

    # Linking
    camRgb.preview.link(manip.inputImage)
    manip.out.link(videoEnc.input)
    videoEnc.bitstream.link(xout.input)

    # Connect to device and start pipeline
    try:
        with dai.Device(pipeline) as device:
            
            # Output queue will be used to get the encoded data from the output defined above
            q = device.getOutputQueue(name="raw", maxSize=30, blocking=False)

            # stream_process = open_stream_process()

            print("OAK Open")
            try:
                while True:
                    connections = list(server.websockets)
                    if connections:
                        packet = q.get()  # Blocking call, will wait until a new data has arrived
                        # stream_process.stdin.write(h265Packet.getData().tobytes())
                        img_bytes = packet.getData().tobytes()
                        imgBASE64 = b64encode(img_bytes)
                        imgBASE64_string = imgBASE64.decode('utf-8')
                        print(dai.Clock.now() - packet.getTimestamp(), end = '\r')
                        # Have to iterate with index because the array changes size during iteration
                        for index in range(len(connections)):
                            try:
                                await connections[index].send(json.dumps({'img':imgBASE64_string}))
                                # print("sent frame %d to %s" % (packet.getSequenceNum(), str(connections[index])))
                            except websockets.exceptions.ConnectionClosedOK:
                                pass
                            except IndexError:
                                pass
                        await asyncio.sleep(0.01)
                    else:
                        await asyncio.sleep(1)

            except KeyboardInterrupt:
                pass
    except RuntimeError:
        print("Unable to talk with oak camera")
        oak = False

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
