#ifndef BTComm
#define BTComm

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

struct msg_byte{
  byte full_byte;
  byte lower_nibble;
  byte upper_nibble;
};

struct FullBtMsg{
 msg_byte command_byte; // byte 0
 msg_byte detail_byte; // byte 1 
 msg_byte Kp_byte; // byte 2 
 msg_byte Ki_byte; // byte 3 
 msg_byte Kd_byte; // byte 4 
 msg_byte algo_byte; // byte 5 
 msg_byte overflow_byte; // byte 6
 msg_byte status_byte; // byte 7
};

struct SanityChecks {
  const byte BT_echo = 0b1000;
  const byte Servo_Pos = 0b1001;
  const byte Sensor_Read = 0b1010;
  const byte Tilt_Measure = 0b1011;
};

struct ServoCommand {
 byte cmd;
 byte pos; 
};

struct ServoLookupTbl {
 const ServoCommand angle_90 = {0b0000,90};
 const ServoCommand angle_60 = {0b0000,60};
 const ServoCommand angle_30 = {0b0000,30};
 const ServoCommand angle_0 = {0b0000,0};  // center position on servo
 const ServoCommand angle_120 = {0b0000,120};
 const ServoCommand angle_150 = {0b0000,150};
 const ServoCommand angle_180 = {0b0000,180};
};
    
class BTComm_Standard {
  public:
    BTComm_Standard();
    //struct msg_byte out_byte;
    boolean isSanityCheck;
    FullBtMsg request;
    FullBtMsg response;
    // Constructor
    
    // Methods
    // function vairables/arguments in C can be passed in as either
    // references or values. Passing in the array is only a reference
    // so the length of the array must be passed in as a value.
    FullBtMsg Process_Request(byte pi_request[], byte length);
    boolean checkRequestType(byte command_byte);
    
  private:
};
#endif
