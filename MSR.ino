#include <Servo.h>

Servo rightMotor;
Servo leftMotor;
Servo verticalMotor;

const int RIGHT_PIN = 9;
const int LEFT_PIN = 10;
const int VERT_PIN = 11;

const float HORZ_LIMIT = 0.5;
const float VERT_LIMIT = 1.0;

String inputString = "";
bool stringComplete = false;
float surge = 0.0;
float yaw = 0.0;
float heave = 0.0;

void setup() {
  Serial.begin(115200);
  
  rightMotor.attach(RIGHT_PIN);
  leftMotor.attach(LEFT_PIN);
  verticalMotor.attach(VERT_PIN);

  stopAll();
  delay(3000);
}

void loop() {
  if (stringComplete) {
    parseData(inputString);
    inputString = "";
    stringComplete = false;
    updateMotors();
  }
}

void updateMotors() {
  float s = surge * HORZ_LIMIT;
  float y = yaw * HORZ_LIMIT;
  float h = heave * VERT_LIMIT;

  float rightSpeed = s - y;
  float leftSpeed  = s + y;
  float vertSpeed  = h;

  writeMotor(rightMotor, rightSpeed);
  writeMotor(leftMotor, leftSpeed);
  writeMotor(verticalMotor, vertSpeed);
}

void writeMotor(Servo &motor, float val) {
  if (val > 1.0) val = 1.0;
  if (val < -1.0) val = -1.0;

  int pwm = 1500 + (val * 400);
  motor.writeMicroseconds(pwm);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') stringComplete = true;
  }
}

void parseData(String data) {
  int sInd = data.indexOf("S:");
  int yInd = data.indexOf("Y:");
  int hInd = data.indexOf("H:");
  
  if (sInd > -1 && yInd > -1 && hInd > -1) {
    surge = data.substring(sInd+2, data.indexOf(',', sInd)).toFloat();
    yaw   = data.substring(yInd+2, data.indexOf(',', yInd)).toFloat();
    heave = data.substring(hInd+2).toFloat();
  }
}

void stopAll() {
  rightMotor.writeMicroseconds(1500);
  leftMotor.writeMicroseconds(1500);
  verticalMotor.writeMicroseconds(1500);
}
