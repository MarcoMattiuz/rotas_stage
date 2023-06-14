import asyncio
import json
import websockets.server
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from base64 import b64encode
import cv2
import numpy as np
import depthai as dai
from depthai import NNData
from depthai_sdk.classes import Detections
from os import listdir

from pigpio.config import *

BROADCAST_RATE = 3

server = None

oak = True

granted = None

active = True

AUDIODIR = './web/audio/'
AUDIOFORMAT = '%s.mp3'

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

# WebSocket message receive and send
async def on_message(websocket):
    try:
        async for message in websocket:
            print(message, websocket)
            try:
                msg = json.loads(message)
            except json.decoder.JSONDecodeError:
                print(message, "DECODE ERROR")
                continue

            response = {}

            if controllerCheck(websocket):
                if 'left' in msg.keys():
                    p = int(msg['left']) / 1023
                    leftMotor.power(p)
                
                if 'right' in msg.keys():
                    p = int(msg['right']) / 1023
                    rightMotor.power(p)

                if 'steer' in msg.keys():
                    steer = int(msg['steer']) / 1023

                    try:
                        power = int(msg['accel']) / 1023
                    except KeyError:
                        power = 0
                    
                    motors.steerPower(steer, power)
            else:
                response['permission'] = None

            if 'sound' in msg.keys():
                track = AUDIOFORMAT % msg['sound']

                if track in listdir(AUDIODIR):
                    # This is blocking
                    await asyncio.create_subprocess_shell("mpg321 " + AUDIODIR + track)
                else:
                    # File doesn't exist
                    response['sound'] = None

            if 'img' in msg.keys() and not oak:
                response['img'] = None
            
            if response:
                await websocket.send(json.dumps(response))

    except ConnectionClosedError:
        pass

async def broadcast(websockets, data_to_send):
    if websockets:
        # Have to iterate with index because the array changes size during iteration
        for index in range(len(websockets)):
            try:
                await websockets[index].send(data_to_send)
            except ConnectionClosedOK:
                pass
            except IndexError:
                pass

# Update
async def updater():
    global server

    while active:
        
        if gps.get() != 0:
            await asyncio.sleep(.1)
            continue

        # Build response json
        response = {
            # "batt": {
            #     "level": batt.lvl,
            #     "volts": batt.volts
            # },
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
        await broadcast(list(server.websockets), json.dumps(response))

        await asyncio.sleep(BROADCAST_RATE)


### CAMERA COROUTINES ###
def decode(nn_data: NNData):
    dets = Detections(nn_data)

    layer = nn_data.getFirstLayerFp16()
    results = np.array(layer).reshape((1, 1, -1, 7))

    for result in results[0][0]:
        if result[2] > 0.5:
            dets.add(int(result[1]), result[2], result[3:])

    return dets

async def camera():
    global oak, active

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
    nn.setBlobPath('./roveroak/mobilenet-ssd/mobilenet-ssd.blob')
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

    # Specific mxId for our oak camera
    devinfo = dai.DeviceInfo("14442C1021D88FD000")

    # Connect to device and start pipeline
    try:
        with dai.Device(pipeline, devinfo) as device:
            # Output queue will be used to get the encoded data from the output defined above
            videoQ = device.getOutputQueue(name='video', maxSize=4, blocking=False)
            nnQ = device.getOutputQueue(name='nn', maxSize=4, blocking=False)

            # stream_process = open_stream_process()

            print("OAK Open")
            while active:
                if server.websockets:
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
                    
                    # Encode image - slow: runs on rpi
                    imgJPG_encoded = cv2.imencode('.jpg', videoFrame)[1].tobytes()

                    imgBASE64 = b64encode(imgJPG_encoded)
                    imgBASE64_string = imgBASE64.decode('utf-8')


                    #   {"img": ..., "dets": {"person": 1, "bottle": 2}}
                    data_to_send = {
                        "img": imgBASE64_string
                    }

                    if objects:
                        data_to_send["dets"] = objects

                    await broadcast(list(server.websockets), json.dumps(data_to_send))
                    await asyncio.sleep(0.01)
                else:
                    await asyncio.sleep(1)

    except RuntimeError as e:
        print("Unable to talk with oak camera:\n\t", e)
        oak = False

def controllerCheck(websocket):
    """
    Grants access to the motors only
    to the first websocket that asks for it.
    If that ws disconnects, access will be granted
    to the next websocket that asks for it.
    """

    global granted

    if websocket is granted:
        return True
    elif server.websockets and not granted in server.websockets:
        granted = websocket
        return True
    else:
        return False

#run websocket function
async def main():
    global server, active
    server = await websockets.server.serve(on_message, '0.0.0.0', 8000)
    asyncio.create_task(updater())
    asyncio.create_task(camera())
    print("Ws started")
    await asyncio.Future() # Run forever
    server.close()

# Start the server
asyncio.run(main())
