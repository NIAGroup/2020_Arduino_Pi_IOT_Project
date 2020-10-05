/*
 * Author :  Princton Brennan
 * Purpose : Beginner's Example for Bluetooth Communication 
 * Requirements : 1 LED, Bluetooh Module Hc-05 or newer), an Arduino, &   
 * a Bluetooth Terminal App (or something similar).
 * 
 * Function : The arduino will turn an LED on or off depending on the 
 * commands via Blueooth.
 * 
 * NOTE :: Most LED's that come in kits are rated for 3V, so to be safe place a 150ohm
 * to 250ohm resistor in series with the LED for current limiting. 
 * 
 * HC-05 example : https://create.arduino.cc/projecthub/electropeak/getting-started-with-hc-05-bluetooth-module-arduino-e0ca81
 * 
 * This sketch uses the "SoftwareSerial" Library:
 * 
 * The Arduino hardware has built-in support for serial communication on pins 0 and 1 
 * (which also goes to the computer via the USB connection). The native serial support 
 * happens via a piece of hardware (built into the chip) called a UART. This hardware 
 * allows the Atmega chip to receive serial communication even while working on other 
 * tasks, as long as there room in the 64 byte serial buffer.
 * 
 * The SoftwareSerial library has been developed to allow serial communication on other 
 * digital pins of the Arduino, using software to replicate the functionality (hence the 
 * name "SoftwareSerial"). It is possible to have multiple software serial ports with 
 * speeds up to 115200 bps. A parameter enables inverted signaling for devices which require 
 * that protocol.
 * 
 * For more info : https://www.arduino.cc/en/Reference/softwareSerial
 */
 
#include <SoftwareSerial.h> 
#include <Servo.h>
#include "BT_Communication_Standard.h"

BTComm_Standard btcs; 
const byte servoPin = 6;    // Servo pin assigned as pin 6 [servos require a PWM pin].
Servo servo;                // To create a servo instance, we use the Servo class from Servo.h.

// Using the SoftwareSerial Library, the Digital IO pins 2 & 3 are repurposed as Soft Serial Pins
// NOTE : For wiring the TX pin of the target device/module is connected to the assigned RX pin of the
// Microcontroller, and the RX pin of the target device/module is connected to the assigned TX pin of
// the Microcontroller.  
SoftwareSerial BT_Module(2, 3); // assigned RX , assigned TX 
SoftwareSerial BT_ClassicModule(12, 13); // RX, TX
byte bt_raw_request[8], bt_response[8];
const byte blueLED_pin = 10;   // The led1_pin assigned to pin 10.
const byte yellowLED_pin = 11;   // The led2_pin assigned to pin 11.

// Every Arduino sketch requires at least a setup loop for initializing I/O pins and serial ports
// and a main function called "loop" that will loop indefinitely while the board is powered.
void setup() 
{   
 Serial.begin(9600);       // The default baudrate for the HC-05 is 38400, and 9600 for the HM-10 
 BT_Module.begin(9600);       // If the baudrate is incorrect the messages will not be read/displayed correctly.
 BT_ClassicModule.begin(9600);
 pinMode(blueLED_pin, OUTPUT);      // The led pin gets setup as an output pin. 
 pinMode(yellowLED_pin, OUTPUT);
 servo.attach(servoPin);
 //Serial.println("Ready to connect\nDefualt password is 1234 or 000"); 
} 
void loop() 
{ 
  
 if(BT_ClassicModule.available() > 0){
  Serial.println(BT_ClassicModule.read());
  digitalWrite(blueLED_pin,HIGH); 
  delay(1000);
  for(byte i = 0; i<4;i++){
    digitalWrite(yellowLED_pin,HIGH); 
    delay(500);
    digitalWrite(yellowLED_pin,LOW); 
    delay(500);
  }
 }
 // While there is no incoming data, the Serial available function will return a 0,
 // but when it is receiving data it will no longer be 0. So we wait to read the
 // incoming message before we handle any actions. 
 if (BT_Module.available() > 0)
 { 
     Serial.println("-------------------------------------------------");
     // I believe the way the messages are being sent with the ble code, the messages
     // are being received in 4 byte array lengths. So a second loop is added to ensure
     // no dummy bytes ("0xFF") are processed.
     for(byte i = 0;i<4;i++){
       bt_raw_request[i] = BT_Module.read();
       Serial.print(bt_raw_request[i],HEX);
       Serial.print(":");
     }
     delay(50);
     if (BT_Module.available() > 0)
     {
       for(byte i = 4;i<8;i++){
         bt_raw_request[i] = BT_Module.read();
         Serial.print(bt_raw_request[i],HEX);
         if(i < 7)
         {
           Serial.print(":");
         }
       }
     }
     
     Serial.println("");
     Serial.print("command_byte: ");
     const FullBtMsg request = btcs.Process_Request(bt_raw_request,sizeof(bt_raw_request));
     Serial.println(request.specBytes.command_byte.full_byte, HEX);
     // Serial.print("status_byte: ");
     // Serial.println(request.specBytes.status_byte.full_byte, HEX);
     
     if(btcs.checkRequestType(request.specBytes.command_byte.full_byte)){
       Serial.println("This is a sanity check");
       /* // Test Lines
       Serial.print("full_byte: ");
       Serial.print(request.command_byte.full_byte, HEX);
       Serial.print(", upper: ");
       Serial.print(request.command_byte.nibbles.upper, HEX);
       Serial.print(", lower: ");
       Serial.println(request.command_byte.nibbles.lower,HEX);
       */
       switch(request.specBytes.command_byte.nibbles.upper){
         // BT Echo Sanity Check : Hex - 0x8
         case 8:
           Serial.println("Running BT echo Sanity Check");
           break;
         
         // Servo Position Sanity Check : Hex - 0x9
         case 9:
         // NOTE: When declaring variables in case instructions
         // you have to enclose all the instructions in curly braces.
         // This is because the variable has no scope without the curly braces.
         {
           digitalWrite(yellowLED_pin,HIGH);
           Serial.println("Servo Position Sanity Check");
           byte n = 0;
           while(request.specBytes.command_byte.nibbles.lower != btcs.ServoLookupTbl[n].cmd){
            n++; 
           }
           if(n < 8){
             Serial.print(btcs.ServoLookupTbl[n].cmd);
             Serial.print(":");
             Serial.println(btcs.ServoLookupTbl[n].pos);
             setServoPosition(btcs.ServoLookupTbl[n].pos);
           }
           break;
         }
         
         // Sensor Read Sanity Check : Hex - 0xA
         case 10:
           Serial.println("Sensor Read Sanity Check");
           break;
         
         // Tilt & Measure Sanity Check : Hex - 0xB
         case 11:
           Serial.println("Running Tilt & Measure Sanity Check");
           break;
           
         default:
           Serial.println("Invalid Servo Command.");
           break;
       }
       
     }
     else{
       Serial.println("This is not a sanity check");
     }
     byte response[8];
     for(byte i = 0;i<8;i++){
       response[i] = bt_raw_request[i];
     }
     response[7] = 0x80;
     digitalWrite(blueLED_pin, HIGH);
     for(byte i = 0;i<8;i++){
       BT_Module.write(response[i]);
     }
     delay(1500);
 }
 else
 {
   digitalWrite(blueLED_pin, LOW);
   digitalWrite(yellowLED_pin, LOW); 
 }

}  

void setServoPosition(byte pos){
  // This first condition is for setting the servo position
  if(pos < 181){
    servo.write(pos);
    delay(100); 
  }
  // This next condition is for running a full servo position sweepa
  else{
    for(byte t = 0; t<2; t++){
      for(byte r = 0; r<180; r+=30){
        servo.write(r);
        delay(1000); 
      }
      
      for(byte r = 180; r>0; r-=30){
        servo.write(r);
        delay(1000); 
      }
    }
  }
}
