import paho.mqtt.client as mqtt

# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # #
client_id = 'User001'
topic = "rotas.stage/rover"
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # #
def on_message(client, userdata, message):
    string = str(message.payload.decode("utf-8"))  # stringa ricevuta dall'mqtt
    print(string)

client = mqtt.Client(client_id)
client.connect(broker)
client.on_message = on_message  # attach function to callback
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    client.loop_start()  # start the loop
    client.subscribe(topic)
    while 1:
        pass

except KeyboardInterrupt:
    client.loop_stop()
    print("\nMQTT closed")
    exit()
