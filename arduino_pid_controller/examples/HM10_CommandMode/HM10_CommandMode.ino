#include <SoftwareSerial.h>
SoftwareSerial bt(2,3);

bool nlNeeded = false;

void setup(){
 Serial.begin(9600);
 bt.begin(9600);
 delay(100); 
}

void loop(){
 if (Serial.available()>0){
  bt.write(Serial.read()); 
  nlNeeded = true;
 } 
 else{
  if (nlNeeded){
    Serial.println(""); 
    nlNeeded = false;
  } 
 }
 while (bt.available()>0){
  Serial.write(bt.read());
 }
 
}
