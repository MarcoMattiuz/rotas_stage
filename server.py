import base64
import cv2
import multiprocessing as mp
import asyncio
import websockets
import json
import subprocess
import depthai as dai
import threading
import numpy as np
import pwmraspberry as pwm
# import server as serv
# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)

xout.setStreamName("disparity")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)

# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_threadRunning = True
_webcamOn = True
_auth = 0 

_ThreadIsRunning = False
def change_speed(speed):
    global _speed
    global _steering
    _speed = int(speed)
    pwm.traz(_speed, _steering)


def change_steering(steering):
    global _speed
    global _steering
    _steering = int(steering)
    pwm.traz(_speed, _steering)


def change_camera(camera):
    global _camera
    _camera = camera
    pwm.set_camera(_camera)

# # # # # # # # VIDEO CAM # # # # # # # #
device = dai.Device(pipeline) 
q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)


# cam = cv2.VideoCapture(3)
# cam.set(3, 320)
# cam.set(4, 240)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

async def send_frames(websocket):
    global _webcamOn
    global cam
    while _webcamOn:
        # frame = cam.read()[1]
        inDisparity = q.get()  # blocking call, will wait until a new data has arrived
        frame = inDisparity.getFrame()
        frame = cv2.flip(frame, 0)
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_PLASMA)
        print(frame)

        imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
        imgBASE64 = base64.b64encode(imgJPG_encoded)
        imgBASE64_string = imgBASE64.decode('utf-8')
        await websocket.send(json.dumps({'photo':imgBASE64_string}))
   

# def sendCallBack_frames():
#     while _cThreadIsRunning:
#         print("webs: ")

async def on_message(messag):
    print(messag)
    if "speed" in messag:
        change_speed(messag["speed"])
        print(f"speed: {_speed} steerind: {_steering}")
    elif "steering" in messag:
        change_steering(messag["steering"])
        print(f"speed: {_speed} steering: {_steering}")
    elif "camera" in messag:
        change_camera(messag["camera"])
        print(f"camera: {_camera}")
    
async def server(websocket, path):

    async def receive():
        global _threadRunning
        global _auth
        while _webcamOn: 
            message = await websocket.recv()
            message = json.loads(message)
            if "username" in message:
                if message['username']=='admin':
                    _auth=1
                    if "password" in message:
                        if message['password']=='rotas88':
                            _auth=2
                            await websocket.send(json.dumps({"login":"logged"}))
                        else:
                            await websocket.send(json.dumps({"error":"Wrong password or password"}))    
                else:
                    await websocket.send(json.dumps({"error":"Wrong username or password"}))
            if _auth==2 :
                if 'photo' in message:
                    if message['photo']==1:
                        _thread = threading.Thread(target=asyncio.run, args=(send_frames(websocket),))
                        _thread.start()
                        _threadRunning=False

                await on_message(message)
    
    receive_result= await asyncio.gather(receive())            

start_server = websockets.serve(server, "192.168.8.155", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
