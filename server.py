

import pwmraspberry as pwm
import asyncio
import websockets
import json
import subprocess
# 192.168.9.245
#subprocess.Popen(["python", "/var/www/html/camera.py"])
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
    global _speedte
    global _steering
    _steering = int(steering)
    pwm.traz(_speed, _steering)


def change_camera(camera):
    global _camera
    _camera = camera
    pwm.set_camera(_camera)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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


async def server(websocket, path):
    global _auth
    await websocket.send(".")
   
    while True:
        message = await websocket.recv()
        message = json.loads(message)

        #only for login
        if "username" in message:
            if message['username']=='admin':
                _auth=1
                if "password" in message:
                    if message['password']=='rotas88':
                        _auth=2
                        await websocket.send("logged")
                    else:
                        await websocket.send("Wrong username or password")
            else:
                await websocket.send("Wrong username or password")
        print(_auth)
        if _auth==0 :
            on_message(message)


start_server = websockets.serve(server, "0.0.0.0", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
