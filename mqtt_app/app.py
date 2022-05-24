import os
import eel
from win32api import GetSystemMetrics

import paho.mqtt.client as mqtt
from time import sleep
# non funziona su linux o mac

# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #

def change_speed(speed):
    print(speed)


def change_steering(steering):
    print(steering)


def change_camera(camera):
    print(camera)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # #
client_id = 'RoverRotas_rover'
topic = "rotas.stage/rover"
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # #


def on_message(client, userdata, message):
    string = str(message.payload.decode("utf-8"))  # stringa ricevuta dall'mqtt
    if string.find("speed"):
        change_speed(string[-2:])
    elif string.find("steering"):
        change_steering(string[-2:])
    elif string.find("camera"):
        change_camera(string[-2:])


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
    client.publish(topic, f"speed: {speed}")


@eel.expose
def changeCamera(camera):
    camera = int(camera)
    if camera > 0:
        camera = f"0{camera}"
    client.publish(topic, f"camera: {camera}")


@eel.expose
def changeSteering(steering):
    steering = int(steering)
    if steering > 0:
        steering = f"0{steering}"
    client.publish(topic, f"steering: {steering}")


eel.start('index.html',
          size=(GetSystemMetrics(0)-200, GetSystemMetrics(1)-200),
          position=(100, 100))
