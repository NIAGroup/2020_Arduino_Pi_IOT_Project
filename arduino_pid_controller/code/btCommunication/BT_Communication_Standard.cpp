#include "BT_Communication_Standard.h"


BTComm_Standard::BTComm_Standard(){
 // default code
} 

FullBtMsg BTComm_Standard::Process_Request(byte pi_request[], byte length){
  FullBtMsg request;
  for(byte i = 0; i< length;i++){
   request.full_msg[i].full_byte = pi_request[i]; 
  }
  return request;
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

