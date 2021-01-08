#include <Servo.h>
#include <SharpIR.h>

SharpIR SharpIR( SharpIR::GP2Y0A21YK0F, A0 );

const byte servoPin = 5;    // Servo pin assigned as pin 6 [servos require a PWM pin].
Servo servo;           

char x;
unsigned long eventInterval = 250;
unsigned int previousDistance;
unsigned int currentDistance;
unsigned long previousTime = 0;
unsigned long currentTime = millis();
int currentServoPosition = 90; // sets the balance beam parallel to the surface
int targetServoPosition;
String startMsg = "################################\n" \
                  "  running Servo/Sensor Example  \n" \
                  "################################";

// When the ball is too far left, the lower the error 
// When the ball is too far right, the greater the error           

double Kp, Ki, Kd; // PID controller constants
double previousError, currentError;
double P, I, D, PID_out; 
const byte setpoint = 16;

// Variables to use for calculating the min & max values
const int max_angle = 120; 
const int min_angle = 60; 
const int max_distance = 20; 
const int min_distance = 9; 
const int min_error = setpoint - max_distance;
const int max_error = setpoint - min_distance;
double min_P, min_I, min_D, min_PID;
double max_P, max_I, max_D, max_PID;

void setup(){
 Serial.begin(9600); 
 servo.attach(servoPin);
 
 delay(500);
 //servo.write(currentServoPosition);
 Serial.println(startMsg);
 Kp = 1;
 Ki = 0;
 Kd = 1;
 servo.write(currentServoPosition);
 //eventInterval = 2000;
 //runTimer(millis());
}

void loop(){
  if (Serial.available() > 0){
    x = Serial.read();
    Serial.print("new msg: ");
    Serial.println(x);
    switch (x){
     case '1':
       targetServoPosition = 0;
       Serial.println("Servo set to 0 degrees.");
       runTimer(millis());
       break;
     case '2':
       targetServoPosition = 30;
       Serial.println("Servo set to 30 degrees.");
       runTimer(millis());
       break;
     case '3':
       targetServoPosition = 60;
       Serial.println("Servo set to 60 degrees.");
       updateServoPosition();
       runTimer(millis());
       break;
     case '4':
       targetServoPosition = 90;
       Serial.println("Servo set to 90 degrees.");
       updateServoPosition();
       runTimer(millis());
       break;
     case '5':
       targetServoPosition = 120;
       Serial.println("Servo set to 120 degrees.");
       updateServoPosition();
       runTimer(millis());
       break;
     case '6':
       targetServoPosition = 150;
       Serial.println("Servo set to 150 degrees.");
       updateServoPosition();
       runTimer(millis());
       break;
     case '7':
       targetServoPosition = 180;
       Serial.println("Servo set to 180 degrees.");
       updateServoPosition();
       runTimer(millis());
       break;
     case '8':
       runTimer(millis());
       break;
    }
    
  }
  //PID_control();
}

void getPIDLimits(){
  min_P = Kp * min_error;
  max_P = Kp * max_error;
  //min_D = Kd event
}

void updateServoPosition(){
  if (targetServoPosition > currentServoPosition){
    for(currentServoPosition = currentServoPosition; currentServoPosition < targetServoPosition; currentServoPosition+=5){
      servo.write(currentServoPosition);
      delay(100);
    }
    
  } else if (targetServoPosition < currentServoPosition) {
    for(currentServoPosition = currentServoPosition; currentServoPosition > targetServoPosition; currentServoPosition-=5){
      servo.write(currentServoPosition);
      delay(100);
    }
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
  currentServoPosition = (int)map(PID_out,min_error,max_error,min_angle,max_angle);
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
   distance += SharpIR.getDistance();
   i+=1;
   currentTime = millis();
 }
 return (unsigned int)distance/i;
}

void runTimer(unsigned long startTime){
 float  i = 0;
 int distance = 0;
 currentTime = startTime;
 while (currentTime - startTime < eventInterval){
   /*Serial.print("currentTime:");
   Serial.print(currentTime);
   Serial.print(", Delta: ");
   Serial.println(currentTime - startTime);*/
   distance += (int)(SharpIR.getDistance()); //Compensate for conversion from inches to cm.
   Serial.print("\t\t");
   Serial.println((int)(SharpIR.getDistance()));
   i+=1;
   currentTime = millis();
 }
   
   Serial.print("\nDistance: ");
   Serial.print((int)(distance/i));
   Serial.println("cm");
   Serial.print("start time: "); 
   Serial.print(startTime); 
   Serial.print(", current time: "); 
   Serial.print(currentTime);
   Serial.print(", previous time: ");
   Serial.println(previousTime);
}
