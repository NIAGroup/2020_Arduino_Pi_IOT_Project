#include "BT_Communication_Standard.h"



BTComm_Standard::BTComm_Standard(){
 // default code
} 

byte BTComm_Standard::Process_Request(byte pi_request[8]){
  command_byte = pi_request[0];
  //Serial.println("");
  //Serial.print("command_byte: ");
  //Serial.println(command_byte, HEX);
  
  /*
  byte upper_nibble = command_byte & 0b11110000;  // Masking lower 4 bits to focus on the upper 4 bits
  byte lower_nibble = command_byte & 0b00001111;
  upper_nibble = upper_nibble >> 4;
  */
  return command_byte;
}

boolean BTComm_Standard::checkRequestType(byte command_byte){
  byte upper_nibble = command_byte & 0b10000000;
  upper_nibble = upper_nibble >> 7;
  byte return_bit = 0;
  if (upper_nibble == 0){
    return_bit = 0;
  }
  else{
    return_bit = 1;
  }
  return return_bit;
}

