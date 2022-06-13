
#import cv2
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
            try:
                message = await websocket.recv()
                message = json.loads(message)
                if "u" in message:
                    if message['u']=='admin':
                        _auth=1
                        if "p" in message:
                            if message['p']=='rotas88':
                                _auth=2
                                await websocket.send("logged")
                    else:
                            await websocket.send("Wrong password or password")    
                else:
                    await websocket.send("Wrong username or password")      
                if _auth==2 :
                    await on_message(message)
            except websockets.exceptions.ConnectionClosedError as e:
                raise Exception(f'Websocket closed {e.code}')
                break
            except Exception:
                raise Exception('Not a websocket')
    
    receive_result= await asyncio.gather(receive())            

start_server = websockets.serve(server, "0.0.0.0", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
