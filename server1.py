

# import websockets
# import asyncio
# import base64
# import json
# import logging
# import cv2

# FRAMES_PER_BUFFER = 3200

# CHANNELS = 1
# RATE = 16000


# # starts recording
# stream = p.open(

#    channels=CHANNELS,
#    rate=RATE,
#    input=True,
#    frames_per_buffer=FRAMES_PER_BUFFER
# )

# # the AssemblyAI endpoint we're going to hit
# URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
# auth_key = "xxxxxx"
# cap = cv2.VideoCapture(0)
# font = cv2.FONT_HERSHEY_SIMPLEX
# text = ""
# webcamIsOn = True


# async def send_receive():
#     print(f'Connecting websocket to url ${URL}')
#     async with websockets.connect as _ws:
#         await asyncio.sleep(0.1)
#         print("Receiving SessionBegins ...")
#         session_begins = await _ws.recv()
#         print(session_begins)
#         print("Sending messages ...")

#         async def send():
#             while True:
#                 try:
#                     data = stream.read(FRAMES_PER_BUFFER)
#                     data = base64.b64encode(data).decode("utf-8")
#                     json_data = json.dumps({"audio_data": str(data)})
#                     await _ws.send(json_data)
#                 except websockets.exceptions.ConnectionClosedError as e:
#                     logging.exception(f'Websocket closed {e.code}')
#                     break
#                 except Exception:
#                     logging.exception('Not a websocket')
#                 await asyncio.sleep(0.01)
#             return True

#         async def receive():
#             global text
#             while True:
#                 try:
#                     result_str = await _ws.recv()
#                     text = json.loads(result_str)['text']
#                     print(text)
#                 except websockets.exceptions.ConnectionClosedError as e:
#                     logging.exception(f'Websocket closed {e.code}')
#                     break
#                 except Exception:
#                     logging.exception('Not a websocket')

#         async def webcam():
#             global text, webcamIsOn
#             while webcamIsOn:
#                 ret, frame = cap.read()

#                 if text:
#                     cv2.putText(frame, text, (50, 425), font, 1, (0, 255, 255), 2, cv2.LINE_4)
#                 cv2.imshow("Webcam", frame)

#                 if cv2.waitKey(1) & 0xFF == 27:  # use ESC to quit
#                     webcamIsOn = False
#                     cap.release()
#                     cv2.destroyAllWindows()
#                 await asyncio.sleep(0.01)

#         send_result, receive_result, webcam_result = await asyncio.gather(send(), receive(), webcam())

# asyncio.run(send_receive())