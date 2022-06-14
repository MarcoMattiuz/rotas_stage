#import cv2
import asyncio
import websockets
import json
import subprocess
import cv2
import numpy as np
import pwmraspberry as pwm
subprocess.Popen(["python", "/var/www/html/camera.py"])
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
        global _auth
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
            if _auth==2 :
                await on_message(message)
    
    receive_result= await asyncio.gather(receive())            

start_server = websockets.serve(server, "0.0.0.0", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
