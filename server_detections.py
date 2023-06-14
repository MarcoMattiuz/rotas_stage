import asyncio
import json
import websockets.server
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.legacy.server import WebSocketServerProtocol
from base64 import b64encode
import numpy as np
import depthai as dai
from depthai import NNData
from depthai_sdk.classes import Detections
from os import listdir
import logging

from roveroak.oak import create_pipeline
from pigpio.config import *

BROADCAST_RATE = 3

server = None

oak = True
"""
This flag indicates if the oak camera is ready.\n
It can be used to restart the camera
"""

granted = None
"""
Stores the websocket which has control rights
"""

busato = True
"""
Busato is a guy who loves while True statements
"""

AUDIODIR = './web/audio/'
MP3_FORMAT = '%s.mp3'
PLAYER = 'mpg321'
PLAYCMD = PLAYER + ' ' + AUDIODIR + MP3_FORMAT + ' > /dev/null 2>&1'

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
"""
mobilenet-ssd detection labels
"""

async def on_message(websocket: WebSocketServerProtocol):
    """
    Websocket event handler
    """
    global oak, busato

    try:
        async for message in websocket:
            logging.info(message + ' from ' + str(websocket.remote_address))

            try:
                msg = json.loads(message)
            except json.decoder.JSONDecodeError:
                logging.warning("DECODE ERROR")
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

                # Oak camera controls
                if 'oak' in msg.keys():
                    oak_command = msg['oak']
                    if isinstance(oak_command, bool):
                        oak = oak_command
                    # TODO: Implement resize

                # Server controls
                if 'active' in msg.keys() and not msg['active']:
                    # Stop the server
                    busato = False

            else:
                response['permission'] = None

            if 'sound' in msg.keys():
                track = msg['sound']

                if MP3_FORMAT % track in listdir(AUDIODIR):
                    await asyncio.create_subprocess_shell(PLAYCMD % track)
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

    while busato:
        
        if not server.websockets:
            await asyncio.sleep(1)
            continue

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
        if response:
            logging.info("Sending data: " + str(response))
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
    global oak, busato

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

    # Resizer setup
    manip = pipeline.create(dai.node.ImageManip)
    # 480p 16:9 frames
    manip.initialConfig.setResize(832, 480)
    # NV12 frames are supported by video encoder
    manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
    manip.setMaxOutputFrameSize(2000000)

    # Video Encoder setup
    videoEnc = pipeline.create(dai.node.VideoEncoder)
    videoEnc.setDefaultProfilePreset(20, dai.VideoEncoderProperties.Profile.MJPEG)
    # videoEnc.setBitrateKbps(100)

    # Links
    videoOut = pipeline.create(dai.node.XLinkOut)
    videoOut.setStreamName('video')
    nnOut = pipeline.create(dai.node.XLinkOut)
    nnOut.setStreamName('nn')

    # Linking
    cam.video.link(manip.inputImage)
    manip.out.link(videoEnc.input)
    videoEnc.bitstream.link(videoOut.input)

    cam.preview.link(nn.input)
    nn.out.link(nnOut.input)

    # Connect to device and start pipeline
    while busato:
        try:
            # Specific mxId for our oak camera
            with dai.Device(pipeline, dai.DeviceInfo("14442C1021D88FD000")) as device:
                # Output queue will be used to get the encoded data from the output defined above
                videoQ = device.getOutputQueue(name='video', maxSize=30, blocking=False)
                nnQ = device.getOutputQueue(name='nn', maxSize=4, blocking=False)

                # To do the stream with ffmpeg/vlc/rtmp server
                # stream_process = open_stream_process()

                logging.info("OAK Open")
                while busato and oak:
                    if server.websockets:
                        # Write data to the streaming process
                        # stream_process.stdin.write(videoQ.get().getData().tobytes())

                        # Get data from neural network
                        nnData: NNData = nnQ.get()
                        
                        # Latency meter
                        # logging.log(dai.Clock.now() - nnData.getTimestamp(), end = '\r')
                        
                        # THIS SHIT CAN BE DONE ONBOARD!!!
                        dets: Detections = decode(nnData)
                        
                        objects = {}

                        if len(dets.detections) > 0:
                            for det in dets.detections:
                                det: dai.ImgDetection
                                
                                # TODO: serialize this stuff and 
                                # send it along with mjpeg frame.
                                # Draw the bounding boxes
                                # on the client side.

                                # Continue if it is not so confident
                                # This should be done during neuralnetwork setup
                                # check if nn.setConfidenceThreshold(.5) exists
                                if det.confidence < .5: continue

                                label = labels[det.label]
                                if label in objects.keys():
                                    objects[label] += 1
                                else:
                                    objects[label] = 1

                        # Get data from encoded bitstream
                        videoPacket = videoQ.get()
                        MJPEGFrame = videoPacket.getData().tobytes()
                        
                        imgBASE64 = b64encode(MJPEGFrame).decode('utf-8')

                        #   {"img": ..., "dets": {"person": 1, "bottle": 2}}
                        data_to_send = {
                            "img": imgBASE64
                        }

                        if objects:
                            data_to_send["dets"] = objects

                        await broadcast(list(server.websockets), json.dumps(data_to_send))
                        await asyncio.sleep(0.01)
                    else:
                        await asyncio.sleep(1)

        except RuntimeError as e:
            logging.warning("Unable to talk with oak camera: " + str(e))
            
            # Oak camera is not available
            oak = False

            # Wait for reinitialization request
            while not oak and busato:
                await asyncio.sleep(1)
            
            logging.info("Restarting oak camera")
    

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

async def main():
    global server, busato
    
    # First, try connecting to the JBL
    await asyncio.create_subprocess_shell("bluetoothctl connect 30:C0:1B:C8:DF:4B")

    # Initialize server listening
    server = await websockets.server.serve(on_message, '0.0.0.0', 8000)
    
    # Start tasks
    asyncio.create_task(updater())
    asyncio.create_task(camera())

    # Ready to rock
    logging.info("Rover started")
    
    # Say it's all ready
    await asyncio.create_subprocess_shell(PLAYCMD % 'marco' + ' && ' + PLAYCMD % 'acceso')

    while busato:
        await asyncio.sleep(1)

    server.close()

    # Say goodbye

# Start the server
asyncio.run(main())