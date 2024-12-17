// Define stepper motor connections:
#define dirPin 2
#define stepPin 3
#define dirPin1 4
#define stepPin1 5
#define solenoidPin 6
#define motorInterfaceType 1
#include <ezButton.h>
#include <AccelStepper.h>
#include <Wire.h>
#include <avr/wdt.h>

#define MAX_POSITION 0x7FFFFFFF  // maximum of position we can set (long type)

ezButton limitSwitch(A0);  // create ezButton object that attach to pin A0;
ezButton limitSwitch1(A1);
ezButton limitSwitch2(A2);
ezButton limitSwitch3(A3);

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);

// Array for X motor (stepper1), handling X positions (0 to 31)
/*int motorStepsX[32] = {
  0, 17.419, 34.838, 52.257, 69.676, 87.095, 104.514, 121.933, 139.352, 156.771,
  174.19, 191.609, 209.028, 226.447, 243.866, 261.285, 278.704, 296.123, 313.542, 330.961,
  348.38, 365.799, 383.218, 400.637, 418.056, 435.475, 452.894, 470.313, 487.732, 505.151,
  522.57, 539.989
};*/
int motorStepsX[32] = {
  53, 50, 47, 43, 38, 36, 33, 31, 27, 22,
  18, 16, 13, 11, 8, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0
};

// Array for Y motor (stepper), handling Y positions (0 to 3)
static int motorStepsY[4] = {
  0, 20, 40, 60
};

// Bools for ME
bool isStopped = false;
bool isStopped1 = false;
bool isBothStopped = false;
bool fire = false;
bool fired = true;  // MY BOOL NO TOUCHY
bool inTheMiddle = false;
bool aimbot = false;
bool isAtTarget = false;
bool atTarget = false;
bool atTarget1 = false;
int middle = 1200;
int middle1 = 200;
int target = 0;
int target1 = 0;
int i = 0;
int j = 0;

// Variables for received X/Y position
int xPosition = -1;
int yPosition = -1;
int delayFire = -1;

void setup() {
  Serial.begin(9600);

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);

  // Set the spinning direction CW/CCW:
  digitalWrite(dirPin, LOW);
  digitalWrite(dirPin1, HIGH);

  pinMode(solenoidPin, OUTPUT);

  limitSwitch.setDebounceTime(10);
  limitSwitch1.setDebounceTime(10);
  limitSwitch2.setDebounceTime(100);
  limitSwitch3.setDebounceTime(100);

  stepper.setMaxSpeed(6000);
  stepper.setAcceleration(4000);
  stepper1.setMaxSpeed(6000);
  stepper1.setAcceleration(4000);

  // Finn custom
  pinMode(13, OUTPUT);
  Wire.begin(8);                 // Initialize I2C with address 8
  Wire.onReceive(receiveEvent);  // Register receive event
  Serial.begin(9600);
}

void(* resetFunc) (void) = 0;
void loop() {

  if (fire) {
    // Wait to fire based on ms
    delay((delayFire));

    digitalWrite(solenoidPin, HIGH);  //Switch Solenoid ON
    delay(1000);                      //Wait 1 Second
    digitalWrite(solenoidPin, LOW);   //Switch Solenoid OFF
    delay(1000);                      //Wait 1 Second
    fired = true;
    fire = false;

    digitalWrite(dirPin, LOW);
    digitalWrite(dirPin1, HIGH);

    resetFunc();
  }

  if (isBothStopped == false) {
    if (isStopped == false) {
      // These four lines result in 1 step:
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
    }
    if (isStopped1 == false) {
      digitalWrite(stepPin1, LOW);
      delayMicroseconds(500);
      digitalWrite(stepPin1, HIGH);
      delayMicroseconds(500);
    }

    limitSwitch.loop();  // MUST call the loop() function first

    if (limitSwitch.isPressed()) {
      digitalWrite(dirPin, HIGH);
      isStopped = true;
      stepper.setCurrentPosition(0);  // Reset motor position to 0
    }

    limitSwitch1.loop();  // MUST call the loop() function first

    if (limitSwitch1.isPressed()) {
      digitalWrite(dirPin1, LOW);
      isStopped1 = true;
      stepper1.setCurrentPosition(0);  // Reset motor position to 0
    }
    if (isStopped == true && isStopped1 == true) {
      isBothStopped = true;
    }

    stepper.run();
    return;
  }
  if (isBothStopped == true && fired) {
    // Set the target position:
    stepper.moveTo(100);
    // Run to target position with set speed and acceleration/deceleration:
    stepper.runToPosition();
    stepper.setCurrentPosition(0);  // Reset motor position to 0

    // Set the target position:
    stepper1.moveTo(-280);
    // Run to target position with set speed and acceleration/deceleration:
    stepper1.runToPosition();
    stepper1.setCurrentPosition(0);  // Reset motor position to 0
    isBothStopped = false;

    fired = false;
  }

  // Move steppers to received X/Y positions
  if ((yPosition >= 0) && (xPosition >= 0)) {
    // KEEP THIS PRINT STATEMENT OR YOU WILL BREAK THIS CODE COMPLETELY
    Serial.println(" ");
    Serial.println(motorStepsY[yPosition], DEC);  // Print X in decimal
    Serial.println(motorStepsX[xPosition], DEC);  // Print X in decimal

    if (((yPosition * 20) + 100) > 160 || ((yPosition * 20) + 100) < 100) {
      Serial.print("yPos Bad!: ");
      //Serial.println(((yPosition * 20) + 100), DEC);  // Print X in decimal
      Serial.println(yPosition, DEC);  // Print X in decimal
      Serial.println(xPosition, DEC);  // Print X in decimal
      stepper.moveTo(0);             // Mapping X to stepper position, adjust the multiplier as needed
    } else { 
      stepper.moveTo(((yPosition * 20)));  // Mapping X to stepper position, adjust the multiplier as needed
    }

    // Move X motor (stepper1) using the X position array
    stepper1.moveTo(-(motorStepsX[xPosition]*8) + 280);  // X motor moves based on xPosition
    //stepper1.moveTo(-((xPosition * 8)) + 280 - 248);  // X motor moves based on xPosition

    stepper.runToPosition();
    stepper1.runToPosition();

    xPosition = -1;
    yPosition = -1;
  }
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    byte receivedData = Wire.read();  // Read incoming data

    // Check if MSB is 1
    if (receivedData & 0b10000000) {  // Check MSB
      // MSB is 1, do "fire" and print remaining bits
      Serial.println("fire");

      // Print remaining bits (7 bits)
      byte remainingBits = receivedData & 0b01111111;  // Mask to get remaining bits
      Serial.print("Remaining Bits: ");
      Serial.println(remainingBits, DEC);  // Print in decimal

      byte delayFire_byte = receivedData & 0b01111111;

      // add calculation for delay in ms
      delayFire = delayFire_byte;

      fire = true;

    } else {
      // MSB is 0, extract the next two bits as Y and print X position
      byte Y = (receivedData >> 5) & 0b00000011;  // Extract bits 6 and 7 for Y
      byte X = receivedData & 0b00011111;         // Get the remaining bits as X (bits 0-4)

      // Store received X and Y positions
      xPosition = X;
      yPosition = Y;
    }
  }
}