#include <Servo.h>

Servo base;         // pin 3
Servo shoulder;     // pin 5
Servo shoulderOpp;  // pin 6 (mirror of shoulder)
Servo elbow;        // pin 9
Servo elbowOpp;     // pin 10 (mirror of elbow)

void setup() {
  Serial.begin(9600);

  base.attach(3, 444, 2600);
  shoulder.attach(5, 444, 2600);
  shoulderOpp.attach(6, 444, 2600);
  elbow.attach(9, 444, 2600);
  elbowOpp.attach(10, 444, 2600);

  // Neutral starting position
  base.write(90);
  shoulder.write(90);
  shoulderOpp.write(90);
  elbow.write(90);
  elbowOpp.write(90);

  Serial.println("System Initialized — Starting Pick and Place Sequence...");
  delay(1000);
}

void loop() {
  // ===== PICK POSITION =====
  Serial.println("\n--- Moving to PICK position ---");
  base.write(90);
  delay(500);

  Serial.println("Lowering arm to pick...");
  moveArmSmooth(110, 130, 15);
  printAngles();
  delay(800);

  Serial.println("Lifting object...");
  moveArmSmooth(60, 80, 15);
  printAngles();
  delay(800);

  // ===== MOVE TO PLACE POSITION =====
  Serial.println("\n--- Rotating base to PLACE position ---");
  for (int b = 90; b >= 0; b -= 2) {
    base.write(b);
    delay(30);
  }

  delay(400);

  // ===== PLACE OBJECT =====
  Serial.println("Placing object...");
  moveArmSmooth(110, 130, 15);
  printAngles();
  delay(800);

  Serial.println("Lifting after placement...");
  moveArmSmooth(60, 80, 15);
  printAngles();
  delay(800);

  // ===== RETURN TO PICK POSITION =====
  Serial.println("\n--- Returning to PICK position ---");
  for (int b = 0; b <= 90; b += 2) {
    base.write(b);
    delay(30);
  }

  Serial.println("Cycle Complete — Repeating...\n");
  delay(2000);
}

// === Smooth shoulder + elbow movement ===
void moveArmSmooth(int shoulderTarget, int elbowTarget, int stepDelay) {
  int shoulderPos = shoulder.read();
  int elbowPos = elbow.read();

  while (shoulderPos != shoulderTarget || elbowPos != elbowTarget) {
    if (shoulderPos < shoulderTarget) shoulderPos++;
    else if (shoulderPos > shoulderTarget) shoulderPos--;

    if (elbowPos < elbowTarget) elbowPos++;
    else if (elbowPos > elbowTarget) elbowPos--;

    shoulder.write(shoulderPos);
    shoulderOpp.write(180 - shoulderPos);
    elbow.write(elbowPos);
    elbowOpp.write(180 - elbowPos);

    delay(stepDelay);
  }
}

// === Print angles of all joints ===
void printAngles() {
  Serial.print("Base: "); Serial.print(base.read()); Serial.print("° | ");
  Serial.print("Shoulder: "); Serial.print(shoulder.read()); Serial.print("° | ");
  Serial.print("Elbow: "); Serial.print(elbow.read()); Serial.println("°");
}
