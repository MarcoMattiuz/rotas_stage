#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "WirelessPoint-Guest";
const char* password = "SNVZTKVZMKB";
const char* mqttServer = "broker.emqx.io";
const char* topic = "rotas.stage/prova";

const int mqttPort = 1883;
const char* mqttUser = "giaco";
const char* mqttPassword = "giaco";

WiFiClient espClient;
PubSubClient client = PubSubClient(espClient);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP32Client", mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }

}

void loop() {
  client.loop();

  delay(1000);
  // client.publish(topic, "Hello");
  // Serial.println("hello");
}

