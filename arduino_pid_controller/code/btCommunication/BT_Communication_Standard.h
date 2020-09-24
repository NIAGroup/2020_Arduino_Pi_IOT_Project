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
