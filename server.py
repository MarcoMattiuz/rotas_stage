import base64
import cv2
import multiprocessing as mp
import asyncio
import websockets
import json
import subprocess
import threading
import numpy as np
#import pwmraspberry as pwm
#subprocess.Popen(["python", "/var/www/html/camera.py"])
# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_threadRunning = True
_webcamOn = True
_auth = 0 
_imgBASE64_string = ""
# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)
_cThreadIsRunning = False
def change_speed(speed):
    global _speed
    global _steering
    _speed = int(speed)
    #pwm.traz(_speed, _steering)


def change_steering(steering):
    global _speed
    global _steering
    _steering = int(steering)
    #pwm.traz(_speed, _steering)


def change_camera(camera):
    global _camera
    _camera = camera
    #pwm.set_camera(_camera)

# # # # # # # # VIDEO CAM # # # # # # # #
cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
async def send_stringBase64(websocket):
    global imgBASE64_string
   

async def send_frames(websocket):
    global _webcamOn
    global cam
    global imgBASE64_string
    while _webcamOn:
        frame = cam.read()[1]
        imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
        imgBASE64 = base64.b64encode(imgJPG_encoded)
        imgBASE64_string = imgBASE64.decode('utf-8')
        await websocket.send(json.dumps({'photo':imgBASE64_string}))
        print("fg")
   

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
    global _auth
    global imgBASE64_string
  
    async def receive():
        global _threadRunning
        global _auth
        while _webcamOn: 
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
                            await websocket.send(json.dumps({"error":"Wrong password or password"}))    
                else:
                    await websocket.send(json.dumps({"error":"Wrong username or password"}))
            if _auth==2 :
                if 'photo' in message:
                    if message['photo']==1:
                        print("thread almost started!!!")
                        _thread = threading.Thread(target=asyncio.run, args=(send_frames(websocket),))
                        _thread.start()
                        print("thread start!!!")
                        _threadRunning=False

                await on_message(message)
    
    receive_result= await asyncio.gather(receive())            

start_server = websockets.serve(server, "192.168.8.46", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
