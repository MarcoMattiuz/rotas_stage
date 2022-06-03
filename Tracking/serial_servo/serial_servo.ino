#include <Servo.h>
#define HORIZONTAL_RESOLUTION 640
// from -320 to 320

String payload;
int pos = 0;
int max_val = int(HORIZONTAL_RESOLUTION / 2);
int min_val = -max_val;

Servo myservo;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  myservo.attach(13);
}

void loop() {
  while (!Serial.available());
  payload = Serial.readString();

  // number = payload.toInt();
  // number++;
  // Serial.println(number);

  pos = map(payload.toInt(), min_val, max_val, 140, 40);
  Serial.println(pos);

  myservo.write(pos);              // tell servo to go to position in variable 'pos'
  delay(15);
}
