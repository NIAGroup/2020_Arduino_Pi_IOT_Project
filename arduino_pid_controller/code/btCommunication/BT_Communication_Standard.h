#ifndef BTComm
#define BTComm

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

union MsgByte{
  byte full_byte;
  struct nibbles{
    byte lower :4;
    byte upper :4;
  }nibbles;
};

union FullBtMsg{
  MsgByte full_msg[8];
  struct specBytes{
   MsgByte command_byte; // byte 0
   MsgByte detail_byte;  // byte 1 
   MsgByte algo_byte;    // byte 2 
   MsgByte Kp_byte;      // byte 3 
   MsgByte Ki_byte;      // byte 4 
   MsgByte Kd_byte;      // byte 5 
   MsgByte reserve_byte; // byte 6
   MsgByte status_byte;  // byte 7
  }specBytes;
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

    
class BTComm_Standard {
  public:
    ServoCommand ServoLookupTbl[4] = {
       {0b0011,80},    //  Hex: 0x3; degrees : tilt right
       {0b0110,90},   //  Hex: 0x0; degrees : 90, center position on servo
       {0b1100,110},  //  Hex: 0xC; degrees : tilt left
       {0b1001,200}   //  Hex: 0x6; sweep : moves the servo from 0 to 180 degrees & back twice
      };
    BTComm_Standard();
    FullBtMsg request;
    FullBtMsg response;
    
    
    // Constructor
    
    // Methods
    // function vairables/arguments in C can be passed in as either
    // references or values. Passing in the array is only a reference
    // so the length of the array must be passed in as a value.
    FullBtMsg Process_Request(byte pi_request[], byte length);
    boolean isSanityCheck(byte command_byte);

    int16_t isValidServoCommand(byte nibble){
      // The length is calculated by finding size of array using sizeof 
      // and then dividing it by size of one element of the array.
      const byte arrayLen = sizeof(ServoLookupTbl)/sizeof(ServoLookupTbl[0]);
      for (int16_t i = 0; i < arrayLen; i++){
        if (int(ServoLookupTbl[i].cmd) == int(nibble)){
          Serial.print("key: ");
          Serial.print(ServoLookupTbl[i].cmd, BIN);
          Serial.print(", nibble: ");
          Serial.print(nibble, BIN);
          Serial.print(", index: ");
          Serial.println(i);
          return i;
        }
      }
      return -1;
    }
    
  private:
};
#endif
