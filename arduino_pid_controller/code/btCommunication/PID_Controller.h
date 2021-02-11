#ifndef pid_ctrlr
#define pid_ctrlr

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include <Servo.h>
#include "BT_Communication_Standard.h"

class PID_Controller {
  public:
    // When the ball is too far left, the lower the error 
    // When the ball is too far right, the greater the error           
    
    double Kp; // PID controller constants
    double Ki;
    double Kd;
    
    double previousError, currentError;
    double P, I, D, PID_out; 
    byte setpoint;
    unsigned int currentBallPosition;
  
    unsigned long eventInterval;
    unsigned int previousDistance;
    unsigned int currentDistance;
    unsigned long previousTime;
    unsigned long currentTime;
    int currentServoPosition; // sets the balance beam parallel to the surface
    int targetServoPosition;

    // Variables to use for calculating the min & max values
    const int max_angle = 110; 
    const int min_angle = 78; 
    const int max_distance = 20; 
    const int min_distance = 9; 
    const int min_error = setpoint - max_distance;
    const int max_error = setpoint - min_distance;

    
    Servo servo;
    
    PID_Controller();
    void runPID_control();
    int getError();
};
#endif
