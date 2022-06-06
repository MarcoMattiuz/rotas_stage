import pwmraspberry as pwm
import asyncio
import websockets
import subprocess
# 192.168.9.245
subprocess.Popen(["python", 'camera.py'])
# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_camera = 0

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


def on_message(string):
    if string.find("speed:0") != -1:
        change_speed(string[-2:])
        print(f"speed: {_speed} steering: {_steering}")
    elif string.find("steering:0") != -1:
        change_steering(string[-2:])
        print(f"speed: {_speed} steering: {_steering}")
    elif string.find("camera:0") != -1:
        change_camera(string[-2:])
        print(f"camera: {_camera}")


async def server(websocket, path):
    while True:
        message = await websocket.recv()
        on_message(message)


start_server = websockets.serve(server, "192.168.8.40", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()