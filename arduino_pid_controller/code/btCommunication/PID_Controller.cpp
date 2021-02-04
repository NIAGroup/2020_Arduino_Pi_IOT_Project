#include "PID_Controller.h"

PID_Controller::PID_Controller(){
 // default code
} 

int PID_Controller::getError(){
 currentDistance = currentBallPosition;
 return (int)setpoint - (int)currentDistance;  
}

void  PID_Controller::runPID_control(){
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
