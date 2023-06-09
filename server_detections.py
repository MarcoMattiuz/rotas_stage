import asyncio
import json
import websockets.server
from serial import Serial
from base64 import b64encode
from time import perf_counter
import cv2
import numpy as np
import depthai as dai
from depthai import NNData
from depthai_sdk.classes import Detections

labels = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor"
]

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

        if 'img' in msg.keys() and not oak:
            await websocket.send(json.dumps({'img': None}))

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

oak = True

def decode(nn_data: NNData):
    dets = Detections(nn_data)

    layer = nn_data.getFirstLayerFp16()
    results = np.array(layer).reshape((1, 1, -1, 7))

    for result in results[0][0]:
        if result[2] > 0.5:
            dets.add(int(result[1]), result[2], result[3:])

    return dets

async def cameraBroadcast():
    global oak

    # Create pipeline
    pipeline = dai.Pipeline()

    # Central camera settings
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam.setFps(20)
    cam.setPreviewSize(300, 300)
    cam.setInterleaved(False)
    cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

    # NeuralNetwork setup
    nn = pipeline.create(dai.node.NeuralNetwork)
    nn.setBlobPath('./mobilenet-ssd/mobilenet-ssd.blob')
    nn.setNumInferenceThreads(2)
    nn.input.setBlocking(False)

    # Links
    videoOut = pipeline.create(dai.node.XLinkOut)
    videoOut.setStreamName('video')
    nnOut = pipeline.create(dai.node.XLinkOut)
    nnOut.setStreamName('nn')

    # Linking
    cam.video.link(videoOut.input)
    cam.preview.link(nn.input)
    nn.out.link(nnOut.input)

    # Connect to device and start pipeline
    try:
        with dai.Device(pipeline) as device:
            
            # Output queue will be used to get the encoded data from the output defined above
            videoQ = device.getOutputQueue(name='video', maxSize=4, blocking=False)
            nnQ = device.getOutputQueue(name='nn', maxSize=4, blocking=False)

            # stream_process = open_stream_process()

            print("OAK Open")
            while True:
                connections = list(server.websockets)
                if connections:
                    # stream_process.stdin.write(h265Packet.getData().tobytes())

                    nnData: NNData = nnQ.get()
                    # print(dai.Clock.now() - nnData.getTimestamp(), end = '\r')
                    dets: Detections = decode(nnData)
                    
                    videoFrame = videoQ.get().getCvFrame()

                    objects = {}

                    if len(dets.detections) > 0:
                        for det in dets.detections:
                            det: dai.ImgDetection
                            label = labels[det.label]
                            if label in objects.keys():
                                objects[label] += 1
                            else:
                                objects[label] = 1

                            # Get frame dimensions (videoFrame is ndarray)
                            height, width, _ = videoFrame.shape

                            # Calculate absolute position for the box
                            box_min = (round(det.xmin * width), round(det.ymin * height))
                            box_max = (round(det.xmax * width), round(det.ymax * height))
                            
                            # Draw the detection box
                            # cv2.rectangle(videoFrame, box_min, box_max, (9,245,5), 2)
                    
                    # Encode image
                    imgJPG_encoded = cv2.imencode('.jpg', videoFrame)[1].tobytes()

                    imgBASE64 = b64encode(imgJPG_encoded)
                    imgBASE64_string = imgBASE64.decode('utf-8')


                    """{"img": ..., "dets": {"person": 1, "bottle": 2}}"""
                    data_to_send = {
                        "img": imgBASE64_string
                    }

                    if objects: 
                        data_to_send["dets"] = objects

                    # Have to iterate with index because the array changes size during iteration
                    for index in range(len(connections)):
                        try:
                            await connections[index].send(json.dumps(data_to_send))
                            # print("sent frame %d to %s" % (packet.getSequenceNum(), str(connections[index])))
                        except websockets.exceptions.ConnectionClosedOK:
                            pass
                        except IndexError:
                            pass
                    await asyncio.sleep(0.01)
                else:
                    await asyncio.sleep(1)

    except RuntimeError as e:
        print("Unable to talk with oak camera:\n\t", e)
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
