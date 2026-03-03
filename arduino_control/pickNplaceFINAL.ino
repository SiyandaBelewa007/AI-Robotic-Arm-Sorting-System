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

// --- Target Angles ---
// Pick [Base, Shoulder, Elbow, Wrist, Hand]
int pickPos[5]  = {15, 50, 41, 145, 26};
// Place [Base, Shoulder, Elbow, Wrist, Hand]
int placePos[5] = {81, 87, 70, 163, 47};

// --- Current Angles ---
int currentPos[5] = {90, 90, 90, 90, 90}; // start from mid positions

// --- Motion Settings ---
int stepDelay = 15;   // delay between steps (ms)
int stepSize  = 1;    // angle increment for smooth motion

void setup() {
  // Attach all servos with extended pulse range for better control
  base.attach(2, 444, 2600);
  shoulder.attach(3, 444, 2600);
  shoulderMirror.attach(4, 444, 2600);
  elbow.attach(5, 444, 2600);
  elbowMirror.attach(6, 444, 2600);
  wrist.attach(9, 444, 2600);
  wristMirror.attach(10, 444, 2600);
  hand.attach(11, 444, 2600);

  Serial.begin(9600);
  Serial.println("Robotic Arm Pick-and-Place Initialized");
}

// --- Helper Function: Smooth Move ---
void moveServoSmooth(Servo &mainServo, Servo &mirrorServo, int &current, int target) {
  int dir = (target > current) ? 1 : -1;
  while (current != target) {
    current += dir * stepSize;
    mainServo.write(current);
    mirrorServo.write(180 - current); // mirror movement
    delay(stepDelay);
  }
}

// --- Helper Function: For single servo (like hand) ---
void moveSingleServoSmooth(Servo &servo, int &current, int target) {
  int dir = (target > current) ? 1 : -1;
  while (current != target) {
    current += dir * stepSize;
    servo.write(current);
    delay(stepDelay);
  }
}

void loop() {
  Serial.println("Performing PICK sequence...");
  // --- PICK Sequence: base -> shoulder -> elbow -> wrist -> hand ---
  moveSingleServoSmooth(base, currentPos[0], pickPos[0]);
  moveServoSmooth(shoulder, shoulderMirror, currentPos[1], pickPos[1]);
  moveServoSmooth(elbow, elbowMirror, currentPos[2], pickPos[2]);
  moveServoSmooth(wrist, wristMirror, currentPos[3], pickPos[3]);
  moveSingleServoSmooth(hand, currentPos[4], pickPos[4]);

  delay(1000); // pause at pick position

  Serial.println("Performing PLACE sequence...");
  // --- PLACE Sequence: shoulder -> base -> elbow -> wrist -> hand ---
  moveServoSmooth(shoulder, shoulderMirror, currentPos[1], placePos[1]);
  moveSingleServoSmooth(base, currentPos[0], placePos[0]);
  moveServoSmooth(elbow, elbowMirror, currentPos[2], placePos[2]);
  moveServoSmooth(wrist, wristMirror, currentPos[3], placePos[3]);
  moveSingleServoSmooth(hand, currentPos[4], placePos[4]);

  delay(1500); // pause at place position

  // Repeat loop
}
