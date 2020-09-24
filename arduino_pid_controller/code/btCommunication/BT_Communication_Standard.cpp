#include "BT_Communication_Standard.h"



BTComm_Standard::BTComm_Standard(){
 // default code
} 

FullBtMsg BTComm_Standard::Process_Request(byte pi_request[], byte length){
  //byte in_byte = pi_request[0];
  FullBtMsg request;
  byte upper_nibble;
  byte lower_nibble;
  //Serial.println(sizeof(pi_request));
  for(byte i = 0;i < length;i++){
    upper_nibble = pi_request[i] & 0b11110000;  // Masking lower 4 bits to focus on the upper 4 bits
    lower_nibble = pi_request[i] & 0b00001111;
    upper_nibble = upper_nibble >> 4;
    switch(i){
     case 0:
      request.command_byte.full_byte = pi_request[i];
      request.command_byte.upper_nibble = upper_nibble;
      request.command_byte.lower_nibble = lower_nibble;
      break; 
     case 1:
      request.detail_byte.full_byte = pi_request[i];
      request.detail_byte.upper_nibble = upper_nibble;
      request.detail_byte.lower_nibble = lower_nibble;
      break; 
     case 2:
      request.Kp_byte.full_byte = pi_request[i];
      request.Kp_byte.upper_nibble = upper_nibble;
      request.Kp_byte.lower_nibble = lower_nibble;
      break; 
     case 3:
      request.Ki_byte.full_byte = pi_request[i];
      request.Ki_byte.upper_nibble = upper_nibble;
      request.Ki_byte.lower_nibble = lower_nibble;
      break; 
     case 4:
      request.Kd_byte.full_byte = pi_request[i];
      request.Kd_byte.upper_nibble = upper_nibble;
      request.Kd_byte.lower_nibble = lower_nibble;
      break; 
     case 5:
      request.algo_byte.full_byte = pi_request[i];
      request.algo_byte.upper_nibble = upper_nibble;
      request.algo_byte.lower_nibble = lower_nibble;
      break; 
     case 6:
      request.overflow_byte.full_byte = pi_request[i];
      request.overflow_byte.upper_nibble = upper_nibble;
      request.overflow_byte.lower_nibble = lower_nibble;
      break;
     case 7:
      request.status_byte.full_byte = pi_request[i];
      request.status_byte.upper_nibble = upper_nibble;
      request.status_byte.lower_nibble = lower_nibble;
      break;  
    }
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

