import paho.mqtt.client as mqtt
# import RPi.GPIO as GPIO   # Import the GPIO library.

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


# # # # # # # # # # # # # # # # # #   MAIN   # # # # # # # # # # # # # # # # # #
try:
    client.loop_start()  # start the loop
    client.subscribe(topic)
    while 1:
        pass

except KeyboardInterrupt:
    client.loop_stop()
    print("\nMQTT closed")
    exit()
