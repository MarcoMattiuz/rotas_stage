import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import pwmraspberry as pwm

# # # # # # # # # # # # # # # #   ROVER TRACTION   # # # # # # # # # # # # # # # #
pwm.setup_pwm()

_speed = 0
_steering = 0
_camera = 0


def change_speed(speed):
    global _speed
    global _steering
    _speed = int(speed)
    pwm.traz(_speed, _steering)
    print(f"speed: {_speed} steering: {_steering}")


def change_steering(steering):
    global _speed
    global _steering
    _steering = int(steering)
    pwm.traz(_speed, _steering)
    print(f"speed: {_speed} steering: {_steering}")


def change_camera(camera):
    global _camera
    _camera = camera
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # #
client_id = 'RoverRotas_rover'
topic = 'rotas.stage/rover'
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # #


def on_message(client, userdata, message):
    string = str(message.payload.decode("utf-8"))  # stringa ricevuta dall'mqtt
    if string.find("speed") != -1:
        change_speed(string[-2:])
        print(f"speed: {_speed} steering: {_steering}")
    elif string.find("steering") != -1:
        change_steering(string[-2:])
        print(f"speed: {_speed} steering: {_steering}")
    elif string.find("camera") != -1:
        change_camera(string[-2:])


client = mqtt.Client(client_id)
client.connect(broker)
client.on_message = on_message  # attach function to callback
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #   MAIN   # # # # # # # # # # # # # # # # # #
try:
    client.loop_start()  # start the loop
    client.subscribe(topic)
    while 1:
        pass

except KeyboardInterrupt:
    client.loop_stop()
    pwm.stop_pwm()
    print("\nMQTT closed")
    exit()
