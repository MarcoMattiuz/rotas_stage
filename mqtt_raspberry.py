import paho.mqtt.client as mqtt
# import RPi.GPIO as GPIO   # Import the GPIO library.

# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # #
client_id = 'UserRotas_rover'
topic = "rotas.stage/rover"
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # #
def on_message(client, userdata, message):
    string = str(message.payload.decode("utf-8"))
    print("Message received: ", string)
    # print("From topic: ", str(message.topic) + "\n")


client = mqtt.Client(client_id)
client.connect(broker)
client.on_message = on_message  # attach function to callback


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
