import paho.mqtt.client as mqtt
from time import sleep

# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # # 
client_id = 'UserRotas0001_rover'
topic = "rotas/rover"
broker = 'broker.emqx.io'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# # # # # # # # # # # # # # # #   MQTT SETUP   # # # # # # # # # # # # # # # # 
def on_message(client, userdata, message):
    print("Message received: ", str(message.payload.decode("utf-8")))
    print("From topic: ", str(message.topic) + "\n")

client = mqtt.Client(client_id)
client.connect(broker)
client.on_message=on_message  #attach function to callback


# # # # # # # # # # # # # # # # # #   MAIN   # # # # # # # # # # # # # # # # # #
try:
    client.loop_start()    #start the loop
    client.subscribe(topic)

    x = 0
    while 1:
        x += 1
        client.publish(topic, f"hello {x}")  # publish
        sleep(3)



except KeyboardInterrupt:
    client.loop_stop()
    print("\nMQTT closed")
    exit()