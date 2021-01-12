/*
 * Author :  Princton Brennan
 * Purpose : Beginner's Example for Servo Control  
 * Requirements : sg90 micro servo (or any 5V servo), an Arduino
 * 
 * Function : The arduino rotate the servo in increments of 30 degrees
 * 
 * This sketch uses the "Servo" Library:
 * 
 * The Arduino hardware has built-in support for serial communication on pins 0 and 1 
 * (which also goes to the computer via the USB connection). The native serial support 
 * happens via a piece of hardware (built into the chip) called a UART. This hardware 
 * allows the Atmega chip to receive serial communication even while working on other 
 * tasks, as long as there room in the 64 byte serial buffer.
 * 
 * This library allows an Arduino board to control RC (hobby) servo motors. Servos have 
 * integrated gears and a shaft that can be precisely controlled. Standard servos allow 
 * the shaft to be positioned at various angles, usually between 0 and 180 degrees. 
 * Continuous rotation servos allow the rotation of the shaft to be set to various speeds.
 * 
 * For more info : https://www.arduino.cc/reference/en/libraries/servo/ 
 * 
 */


#include <Servo.h>

const byte servoPin = 6;    // Servo pin assigned as pin 6 [servos require a PWM pin].
byte servoAngle;            // A servo angle variable it create to set change the servo rotation position.
Servo servo;                // To create a servo instance, we use the Servo class from Servo.h.
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       // Initializing the Serial Monitor to follow along w/ the code.
  servo.attach(servoPin);   // The servo object must be attached to a specific pin.
  servo.write(90);          // The Sg90 has a 180 degree angle of range, so we center it when the code begins.
  delay(1000);              // The delay function is called just to make the rotations easier to follow(this is in milliseconds). 
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Sweep Function:");      // Print statements have been added just to alert the user when each function is running.
  servoFullSweep();                       // This function will sweep full range of the servo's rotation angle, 0 degrees and back to 180 degrees.
  delay(1000);
  Serial.println("Tick Function:");
  servoTicksLoop();                       // This function will start at 180 degrees and decrease by 30 degrees for each tick, then increase by 30 degrees until it's back at its start point.
  delay(1000);
}

// The sweep function will loop a full sweep 4 times.
void servoFullSweep(){
  for(int i = 0;i<4;i++){
    servo.write(0);
    Serial.println("0 degrees");
    delay(1000);
    servo.write(180);
    Serial.println("180 degrees");
    delay(1000);
  }
  
}

// The tick loop function will loop a full the ticking motion back and forth 4 times.
void servoTicksLoop(){
  for(int i=0;i<4;i++){
    for(servoAngle = 180;servoAngle>0;servoAngle-=30){
      servo.write(servoAngle);
      Serial.print(servoAngle);
      Serial.println(" degrees");
      delay(500);
    }
    for(servoAngle = 0;servoAngle<180;servoAngle+=30){
      servo.write(servoAngle);
      Serial.print(servoAngle);
      Serial.println(" degrees");
      delay(500);
    }
  }
  
  
}
