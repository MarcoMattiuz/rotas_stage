import base64
import cv2
#import pwmraspberry as pwm
import multiprocessing
import asyncio
import websockets
import json
import subprocess
# 192.168.8.155
#subprocess.Popen(["python", "/var/www/html/rotas_stage/camera.py"])
# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
_speed = 0
_steering = 0
_camera = 0
_webcamOn = True
_auth = 0 
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
# cam = cv2.VideoCapture(0)
# cam.set(3, 320)
# cam.set(4, 240)    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# async def send_frames(websocket):
#     print("frame")
#     frame = cap.read()[1]
#     imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
#     imgBASE64 = base64.b64encode(imgJPG_encoded)
#     imgBASE64_string = imgBASE64.decode('utf-8')
#     await websocket.send(json.dumps({'photo':imgBASE64_string}))


# def sendCallBack_frames():
#     while _cThreadIsRunning:
#         print("webs: ")

# async def on_message(messag):
#     print(messag)
#     if "speed" in messag:
#         change_speed(messag["speed"])
#         print(f"speed: {_speed} steerind: {_steering}")
#     elif "steering" in messag:
#         change_steering(messag["steering"])
#         print(f"speed: {_speed} steering: {_steering}")
#     elif "camera" in messag:
#         change_camera(messag["camera"])
#         print(f"camera: {_camera}")
    
async def server(websocket, path):
    global _auth
    global _webcamOn
    global _cThreadIsRunning

    message = await websocket.recv()
    
    message = json.loads(message)
    print("message :",message)
    await websocket.send("hi")
    # # frame = cap.read()[1]
    # # imgJPG_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
    # # imgBASE64 = base64.b64encode(imgJPG_encoded)
    # # imgBASE64_string = imgBASE64.decode('utf-8')
    # # await websocket.send(json.dumps({'photo':imgBASE64_string}))
    #     #check if the user can authenticate to the websocket and sends a json format message back
    # if "username" in message:              
    #     if message['username']=='admin':
    #         _auth=1
    #         if "password" in message:
    #             if message['password']=='rotas88':
    #                 _auth=2
    #                 await websocket.send(json.dumps({"login":"logged"}))  
                  
    #             else:
    #                 await websocket.send(json.dumps({"error":"Wrong username or password"}))    
    #     else:
    #         await websocket.send(json.dumps({"error":"Wrong username or password"}))    
    #if _auth==2 :
        #await on_message(message)
async def main():
    async with websockets.serve(server, "192.168.8.46", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())        
