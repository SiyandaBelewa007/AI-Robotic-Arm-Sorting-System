#include <Servo.h>

// --- Servo Declarations ---
Servo base;
Servo shoulder;
Servo shoulderMirror;
Servo elbow;
Servo elbowMirror;
Servo wrist;
Servo wristMirror;
Servo hand;

// --- Potentiometer Pins ---
int potBase = A0;
int potShoulder = A1;
int potElbow = A2;
int potWrist = A3;
int potHand = A4;

// --- Variables ---
int valBase, valShoulder, valElbow, valWrist, valHand;
int angleBase, angleShoulder, angleElbow, angleWrist, angleHand;

void setup() {
  // Attach all servos
  base.attach(2, 444, 2600);
  shoulder.attach(3, 444, 2600);
  shoulderMirror.attach(4, 444, 2600);
  elbow.attach(5, 444, 2600);
  elbowMirror.attach(6, 444, 2600);
  wrist.attach(9, 444, 2600);
  wristMirror.attach(10, 444, 2600);
  hand.attach(11, 444, 2600);

  Serial.begin(9600);
  Serial.println("Robotic Arm Control Initialized");
}

void loop() {
  // --- Read Potentiometers ---
  valBase = analogRead(potBase);
  valShoulder = smoothAnalog(potShoulder);
  valElbow = analogRead(potElbow);
  valWrist = analogRead(potWrist);
  valHand = analogRead(potHand);

  // --- Map Values to Angles (0–180°) ---
  angleBase = map(valBase, 0, 1023, 0, 180);
  angleShoulder = map(valShoulder, 0, 1023, 0, 180);
  angleElbow = map(valElbow, 0, 1023, 0, 180);
  angleWrist = map(valWrist, 0, 1023, 0, 180);
  angleHand = map(valHand, 0, 1023, 0, 180);

  // --- Move Servos ---
  base.write(angleBase);
  shoulder.write(angleShoulder);
  shoulderMirror.write(180 - angleShoulder);  // Mirror movement
  elbow.write(angleElbow);
  elbowMirror.write(180 - angleElbow);        // Mirror movement
  wrist.write(angleWrist);
  wristMirror.write(180 - angleWrist);        // Mirror movement
  hand.write(angleHand);

  // --- Print Values to Serial Monitor ---
  Serial.print("Base: "); Serial.print(angleBase);
  Serial.print(" | Shoulder: "); Serial.print(angleShoulder);
  Serial.print(" | Elbow: "); Serial.print(angleElbow);
  Serial.print(" | Wrist: "); Serial.print(angleWrist);
  Serial.print(" | Hand: "); Serial.print(angleHand);
  Serial.println();

  delay(100); // Small delay for smoother operation
}

int smoothAnalog(int pin) {
  long total = 0;
  for (int i = 0; i < 10; i++) {
    total += analogRead(pin);
    delay(2); // short pause between samples
  }
  return total / 10; // average value
}