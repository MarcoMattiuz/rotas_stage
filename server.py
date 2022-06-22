import base64
from contextlib import nullcontext
import cv2
import multiprocessing as mp
import asyncio
#!/bin/env python
import websockets
import json
import subprocess
import depthai as dai
import threading
import numpy as np
import pwmraspberry as pwm
import contextvars
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

# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_threadRunning = True
_webcamOn = True
_auth = 0 

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
#checks if camera is connected
try:
    device = dai.Device(pipeline) 
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)
except:
    print("camera is not connected")
    _webcamOn = False

#resize the resolution of the camera
def resize_percent(scale_percent, src):

    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    dsize = (width, height)

    output = cv2.resize(src, dsize)
    return output

#message to send
def on_message(messag):
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

#websocket function
async def send_receive(websocket):
        # receive and send the packets
        async def receive():
            global _auth
            global _threadRunning
            while _threadRunning:  
                message = await websocket.recv()
                message = json.loads(message)
                print(message)
                if "username" in message:
                    if message['username']=='admin':
                        _auth=1
                        if "password" in message:
                            if message['password']=='rotas88':
                                _auth=2
                                await websocket.send(json.dumps({"login":"logged"}))
                            else:
                                await websocket.send(json.dumps({"error":"Wrong username or password"}))    
                    else:
                        await websocket.send(json.dumps({"error":"Wrong username or password"}))
                if _auth==2 :
                    on_message(message) 
                    await asyncio.sleep(0.01) 
        #send webcam frames
        async def webcam():
            global _webcamOn
            global _auth
            if(_auth==2):
                while _webcamOn:
                    inDisparity = q.get() 
                    frame = inDisparity.getCvFrame()
                    frame = resize_percent(20,frame)
                    imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
                    imgBASE64 = base64.b64encode(imgJPG_encoded)
                    imgBASE64_string = imgBASE64.decode('utf-8')
                    await websocket.send(json.dumps({'photo':imgBASE64_string}))
                    await asyncio.sleep(0.01) 


        receive_result, webcam_result = await asyncio.gather(receive(), webcam())

async def main():
    async with websockets.serve(send_receive,"192.168.8.155", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())
