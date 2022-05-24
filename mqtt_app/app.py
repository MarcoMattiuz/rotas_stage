import os
import eel
from win32api import GetSystemMetrics

import paho.mqtt.client as mqtt
from time import sleep
# non funziona su linux o mac

# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # #
client_id = 'RoverRotas_rover'
topic = "rotas.stage/rover"
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # #


def on_message(client, userdata, message):
    print("Message received: ", str(message.payload.decode("utf-8")))
    print("From topic: ", str(message.topic) + "\n")


client = mqtt.Client(client_id)
client.connect(broker)
client.on_message = on_message  # attach function to callback
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # #   EEL SETUP   # # # # # # # # # # # # # # # #
absolutepath = os.path.abspath(__file__)
absolutepath = absolutepath[0:-6] + "web"
eel.init(absolutepath)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


client.loop_start()  # start the loop
client.subscribe(topic)


@eel.expose
def changeSpeed(speed):
    speed = int(speed)
    if speed > 0:
        speed = f"0{speed}"
    client.publish(topic, f"Speed: {speed}")


@eel.expose
def changeCamera(camera):
    camera = int(camera)
    if camera > 0:
        camera = f"0{camera}"
    client.publish(topic, f"Camera: {camera}")


@eel.expose
def changeRotation(rotation):
    rotation = int(rotation)
    if rotation > 0:
        rotation = f"0{rotation}"
    client.publish(topic, f"Rotation: {rotation}")


eel.start('index.html',
          size=(GetSystemMetrics(0)-200, GetSystemMetrics(1)-200),
          position=(100, 100))
