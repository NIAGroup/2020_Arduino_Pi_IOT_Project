#ifndef BTComm
#define BTComm

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

class BTComm_Standard {
  public:
    byte command_byte;
    boolean isSanityCheck;
    // Constructor
    BTComm_Standard();
    
    // Methods
    byte Process_Request(byte pi_request[8]);
    boolean checkRequestType(byte command_byte);
    
  private:
};
#endif
