import paho.mqtt.client as mqtt

# # # # # # # # # # # # # # # #   MQTT DATA   # # # # # # # # # # # # # # # # 
username = input("Insert your username: ")
client_id = f'UserRotas{username}_rover'
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
    while 1: pass

except KeyboardInterrupt:
    client.loop_stop()
    print("\nMQTT closed")
    exit()