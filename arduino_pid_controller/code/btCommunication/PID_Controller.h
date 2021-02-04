#ifndef pid_ctrlr
#define pid_ctrlr

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include <Servo.h>

class PID_Controller {
  public:
    // When the ball is too far left, the lower the error 
    // When the ball is too far right, the greater the error           
    
    double Kp, Ki, Kd; // PID controller constants
    double previousError, currentError;
    double P, I, D, PID_out; 
    const byte setpoint = 16;
    unsigned int currentBallPosition;
  
    unsigned long eventInterval = 250;
    unsigned int previousDistance;
    unsigned int currentDistance;
    unsigned long previousTime = 0;
    unsigned long currentTime = millis();
    int currentServoPosition = 90; // sets the balance beam parallel to the surface
    int targetServoPosition;

    // Variables to use for calculating the min & max values
    const int max_angle = 110; 
    const int min_angle = 80; 
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
