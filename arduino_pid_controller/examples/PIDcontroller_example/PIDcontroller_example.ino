#include <Servo.h>
#include <SharpIR.h>

SharpIR SharpIR( SharpIR::GP2Y0A21YK0F, A0 );

const byte servoPin = 5;    // Servo pin assigned as pin 6 [servos require a PWM pin].
Servo servo;           

unsigned long eventInterval = 250;
unsigned int previousDistance;
unsigned int currentDistance;
unsigned long previousTime = 0;
unsigned long currentTime = millis();
int currentServoPosition = 60; // sets the balance beam parallel to the surface
String startMsg = "################################\n" \
                  "  running Servo/Sensor Example  \n" \
                  "################################";

// When the ball is too far left, the error is negative
// When the ball is too far right, the error is positive           

double Kp, Ki, Kd; // PID controller constants
double previousError, currentError;
double P, I, D, PID_out; 
const byte setpoint = 13;

void setup(){
 Serial.begin(9600); 
 servo.attach(servoPin);
 servo.write(0);
 delay(500);
 servo.write(currentServoPosition);
 Serial.println(startMsg);
 Kp = 5;
 Ki = 0;
 Kd = 40;
 //eventInterval = 2000;
 //runTimer(millis());
}

void loop(){
  if (Serial.available() > 0){
    char x = Serial.read();
    switch (x){
     case '1':
       servo.write(0);
       runTimer(millis());
       break;
     case '2':
       servo.write(30);
       runTimer(millis());
       break;
     case '3':
       servo.write(60);
       runTimer(millis());
       break;
     case '4':
       servo.write(90);
       runTimer(millis());
       break;
     case '5':
       servo.write(120);
       runTimer(millis());
       break;
     case '6':
       servo.write(150);
       runTimer(millis());
       break;
     case '7':
       servo.write(180);
       runTimer(millis());
       break;
    }
  }
  PID_control();
  //SeeSawFxn();
}

void SeeSawFxn(){
  byte pos = 0;
  for (pos = 0; pos < 180; pos+=5){
    servo.write(pos);
    delay(100);
  } 
  for (pos = 180; pos > 0; pos-=5){
    servo.write(pos);
    delay(100);
  }
}

void PID_control(){
  currentTime = millis();
  currentError = getError();
  P = Kp*currentError;
  I = I + Ki*currentError;
  D = Kd*((previousError-currentError)/(currentTime-previousTime));
  previousError = currentError;
  previousTime = currentTime;
  previousDistance = currentDistance;
  PID_out = P + I + D;
  currentServoPosition = (int)map(PID_out,-45,30,150,0);
  servo.write(currentServoPosition);
  Serial.println("****************************************************");
  Serial.print("currentDistance: ");
  Serial.print(currentDistance);
  Serial.print(", previousDistance: ");
  Serial.println(previousDistance);
  Serial.print("currentError: "); 
  Serial.print(currentError); 
  Serial.print(", previousError: "); 
  Serial.println(previousError); 
  Serial.print("[P: "); 
  Serial.print(P); 
  Serial.print(", I: "); 
  Serial.print(I); 
  Serial.print(", D: "); 
  Serial.print(D); 
  Serial.print("];\t PID_out: "); 
  Serial.println(PID_out);
  Serial.print("servoPosition: ");
  Serial.println(currentServoPosition);
}

int getError(){
 currentDistance = getPosition();
 return (int)setpoint - (int)currentDistance;  
}

unsigned int getPosition(){
 int  i = 0;
 int distance = 0;
 unsigned long startTime = millis();
 currentTime = startTime;
 while (currentTime - startTime < 100){
   distance += SharpIR.distance();
   i+=1;
   currentTime = millis();
 }
 return (unsigned int)distance/i;
}

void runTimer(unsigned long startTime){
 int  i = 0;
 int distance = 0;
 currentTime = startTime;
 while (currentTime - startTime < eventInterval){
   /*Serial.print("currentTime:");
   Serial.print(currentTime);
   Serial.print(", Delta: ");
   Serial.println(currentTime - startTime);*/
   distance += SharpIR.distance();
   i+=1;
   currentTime = millis();
 }
   
   Serial.print("\nDistance: ");
   Serial.print(distance/i);
   Serial.println("cm");
   Serial.print("start time: "); 
   Serial.print(startTime); 
   Serial.print(", current time: "); 
   Serial.print(currentTime);
   Serial.print(", previous time: ");
   Serial.println(previousTime);
}
