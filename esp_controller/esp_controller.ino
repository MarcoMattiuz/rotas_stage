#include <WiFi.h>
#include <PubSubClient.h>
#define VRx 34
#define VRy 35

/*
const char* ssid = "WirelessPoint-Guest";
const char* password = "SNVZTKVZMKB";
/**/
/*
const char* ssid = "Iphone di Giaco";
const char* password = "12345678";
/**/
/**/
const char* ssid = "Linkem_FCD881_EXT";
const char* password = "d29vust7";
/**/
const char* mqttServer = "broker.emqx.io";
const char* topic = "rotas.stage/rover";
const char* client_name = "ESP32_Client";

const int mqttPort = 1883;

WiFiClient espClient;
PubSubClient client = PubSubClient(espClient);


int speed = 0, steering = 0;
String speed_old = "avanti", steering_old = "dritto";
bool stop = false;

void setup() {
  Serial.begin(115200);
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi.");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected!");

  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect(client_name)) {
      Serial.println("Connected!");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  client.loop();
  speed = analogRead(VRx);
  steering = analogRead(VRy);

  switch (steering) {
    case 4095:
      if (steering_old != "destra") {
        steering_old = "destra";
        stop = false;
        client.publish(topic, "steering: 05");
        Serial.println("destra");
      }
      break;
    case 0:
      if (steering_old != "sinistra") {
        steering_old = "sinistra";
        stop = false;
        client.publish(topic, "steering: -5");
        Serial.println("sinistra");
      }
      break;
    default:
      if (steering_old != "dritto") {
        steering_old = "dritto";
      }
      break;
  }

  switch (speed) {
    case 4095:
      if (speed_old != "avanti") {
        speed_old = "avanti";
        stop = false;
        client.publish(topic, "speed: 05");
        client.publish(topic, "steering: 00");
        Serial.println("avanti");
      }
      break;
    case 0:
      if (speed_old != "indietro") {
        speed_old = "indietro";
        stop = false;
        client.publish(topic, "speed: -5");
        client.publish(topic, "steering: 00");
        Serial.println("indietro");
      }
      break;
    default:
      if (speed_old != "fermo") {
        speed_old = "fermo";
      }
      break;
  }

  if (speed_old == "fermo" && steering_old == "dritto" && stop == false) {
    Serial.println("- STOP -");
    client.publish(topic, "speed: 00");
    client.publish(topic, "steering: 00");
    stop = true;
  }

}
