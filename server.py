import base64
from contextlib import nullcontext
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
_websocket = nullcontext
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
try:
    device = dai.Device(pipeline) 
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)
except:
    print("camera is not connected")

async def send_frames():
    global _webcamOn
    global _websocket
    # if _websocket!=nullcontext:
        # if 'photo' in message:
        #     if message['photo']==1:
    while _webcamOn:
        inDisparity = q.get() 
        frame = inDisparity.getFrame()
        imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
        imgBASE64 = base64.b64encode(imgJPG_encoded)
        imgBASE64_string = imgBASE64.decode('utf-8')
        await _websocket.send(json.dumps({'photo':imgBASE64_string}))

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

async def receive(websocket, path):
    global _threadRunning
    global _auth
    global _websocket
    print(websocket)
    _websocket = websocket
    while _webcamOn:  
        message = await _websocket.recv()
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
           
            await on_message(message)      
   
  

start_server = websockets.serve(receive, "192.168.8.155", 8000)
print(_websocket)
# asyncio.get_event_loop().create_task(send_frames())   
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
