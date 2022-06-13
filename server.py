
#import cv2
import pwmraspberry as pwm
import asyncio
import websockets
import json
import subprocess
from re import S
import cv2
import depthai as dai
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

# Connect to device and start pipeline
device = dai.Device(pipeline) 

# Output queue will be used to get the disparity frames from the outputs defined above
q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
kernel = np.ones((6,6),dtype="uint8")
#kernel = np.ones((6, 6), np.uint8)
inDisparity = q.get()  # blocking call, will wait until a new data has arrived
frame = inDisparity.getFrame()
lenX = len(frame[0])  
lenY = len(frame) 
totals = [0] * 3  
count = int(lenX / 3) 

# def cameraDepth(speed):
#     inDisparity = q.get() 
#     frame = inDisparity.getFrame()
#     frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
#     frame = cv2.erode(frame, kernel, iterations=1)
#     # frame = cv2.dilate(frame, kernel, iterations=1)
#     ret,frame = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)
#     totals = [0] * 3  
#     i=j=0 
#     for i in range(0,int(lenX), 5):
#         for j in range(0,int(lenY), 5):
#             if i<int(lenX/3):
#                 #sinistra 
#                 totals[0] += frame[j][i]
#             elif i >= int(lenX/3) and i<int(lenX/3*2):
#                 #dritt
#                 totals[1] += frame[j][i]
#             elif i >= int(lenX/3*2) and i<int(lenX):
#                 #destr
#                 totals[2] += frame[j][i]
#     mDX = int(totals[0]/count)
#     mFW = int(totals[1]/count)
#     mSX= int(totals[2]/count)
#     minVal = min(mDX,mFW,mSX)
#     print(minVal) 
#     print("SINISTRA",mSX) 
#     print("DESTRA",mDX)
#     print("FORWARD",mFW)  
#     if mFW == 0:  
#         print("--FORWARD")
#         pwm.traz(speed,0)
#     elif mSX == minVal:
#         print("--SINISTRA")
#         pwm.traz(speed,-5)
#     elif mDX == minVal:
#         print("--DESTRA") 
#         pwm.traz(speed,5)
#     else: 
#         pwm.traz(speed,0)
#         print("--FORWARD")
#     frame = cv2.applyColorMap(frame, cv2.COLORMAP_PLASMA)
#     frame = cv2.rectangle(frame, (0,0), (int(lenX/3),400), (255,255,255),3)
#     frame = cv2.rectangle(frame, (int(lenX/3),0), (int(lenX/3*2),400), (255,0,255),3)
#     frame = cv2.rectangle(frame, (int(lenX/3*2),0),(int(lenX),400) , (255,255,0),3)
#     print(frame)
#     cv2.imshow("disparity", frame)
# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_camera = 0
_auth=0

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
    _camera = int(camera)
    pwm.set_camera(_camera)

# # # # # # # # VIDEO CAM # # # # # # # #
# cam = cv2.VideoCapture(0)
# cam.set(3, 320)
# cam.set(4, 240)    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
    global _auth
    async def receive():
        _auth=0
        while True: 
            message = await websocket.recv()
            message = json.loads(message)
            print(message)
            if "username" in message:
                if message['username']=='admin':
                    _auth=1
                    if "password" in message:
                        if message['password']=='rotas88':
                            _auth=2
                            await websocket.send("logged")
                    else:
                        await websocket.send("Wrong password or password")    
                else:
                    await websocket.send("Wrong username or password")        
            print("speeeeeed:",int(message["speed"]))
            inDisparity = q.get() 
            frame = inDisparity.getFrame()
            frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
            frame = cv2.erode(frame, kernel, iterations=1)
            # frame = cv2.dilate(frame, kernel, iterations=1)
            ret,frame = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)
            totals = [0] * 3  
            i=j=0 
            for i in range(0,int(lenX), 5):
                for j in range(0,int(lenY), 5):
                    if i<int(lenX/3):
                        #sinistra 
                        totals[0] += frame[j][i]
                    elif i >= int(lenX/3) and i<int(lenX/3*2):
                        #dritt
                        totals[1] += frame[j][i]
                    elif i >= int(lenX/3*2) and i<int(lenX):
                        #destr
                        totals[2] += frame[j][i]
            mDX = int(totals[0]/count)
            mFW = int(totals[1]/count)
            mSX= int(totals[2]/count)
            minVal = min(mDX,mFW,mSX)
            # print(minVal) 
            # print("SINISTRA",mSX) 
            # print("DESTRA",mDX)
            # print("FORWARD",mFW)  
            if mFW == 0:  
                print("--FORWARD")
                pwm.traz(int(message["speed"]),0)
            elif mSX == minVal:
                print("--SINISTRA")
                pwm.traz(int(message["speed"]),-5)
            elif mDX == minVal:
                print("--DESTRA") 
                pwm.traz(int(message["speed"]),5)
            else: 
                pwm.traz(int(message["speed"]),0)
                print("--FORWARD")
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_PLASMA)
            frame = cv2.rectangle(frame, (0,0), (int(lenX/3),400), (255,255,255),3)
            frame = cv2.rectangle(frame, (int(lenX/3),0), (int(lenX/3*2),400), (255,0,255),3)
            frame = cv2.rectangle(frame, (int(lenX/3*2),0),(int(lenX),400) , (255,255,0),3)
            cv2.imshow("disparity", frame)
            if _auth==2 :
                await on_message(message)
    
    receive_result= await asyncio.gather(receive())            
start_server = websockets.serve(server, "0.0.0.0", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
