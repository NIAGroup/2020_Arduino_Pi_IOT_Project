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
#include <SharpIR.h>
#include "BT_Communication_Standard.h"
#include "PID_Controller.h"

// Every arduino's main sketch should contain a clear boot-up message.
const String startMsg = "################################\n" \
                        "      Starting up to run        \n" \
                        "    Full PID controller code    \n" \
                        "################################";

// Bluetooth variables
BTComm_Standard btcs; 
boolean isDeviceBLE = false;
// Using the SoftwareSerial Library, the Digital IO pins 2 & 3 are repurposed as Soft Serial Pins
// NOTE : For wiring the TX pin of the target device/module is connected to the assigned RX pin of the
// Microcontroller, and the RX pin of the target device/module is connected to the assigned TX pin of
// the Microcontroller.  
SoftwareSerial BT_Module(2, 3); // assigned RX , assigned TX 
SoftwareSerial BT_ClassicModule(12, 13); // RX, TX
byte bt_raw_request[8], bt_response[8];

// Sensor variables
SharpIR SharpIR( SharpIR::GP2Y0A21YK0F, A0 );
unsigned long startTime = 0;
unsigned long previousTime = 0;
unsigned long currentTime = millis();

// Servo variables
const byte servoPin = 5;    // Servo pin assigned as pin 6 [servos require a PWM pin].
Servo servo;                // To create a servo instance, we use the Servo class from Servo.h.

const int max_angle = 110; 
const int min_angle = 80; 
int currentServoPosition = 90; // sets the balance beam parallel to the surface
int targetServoPosition;


// PID Cotnroller object
PID_Controller pid = PID_Controller();

// LED Indicator variables
const byte redLED_pin = 9;   // The red led for error/failure assigned to pin 9.
const byte blueLED_pin = 10;   // The blue led as 1 indicator assigned to pin 10.
const byte yellowLED_pin = 11;   // The yellow led as 1 indicator assigned to pin 11.

// Every Arduino sketch requires at least a setup loop for initializing I/O pins and serial ports
// and a main function called "loop" that will loop indefinitely while the board is powered.
void setup() 
{   
 Serial.begin(9600);       // The default baudrate for the HC-05 is 38400, and 9600 for the HM-10 
 BT_Module.begin(9600);       // If the baudrate is incorrect the messages will not be read/displayed correctly.
 //BT_ClassicModule.begin(9600);
 pinMode(blueLED_pin, OUTPUT);      // The led pin gets setup as an output pin.
 pinMode(redLED_pin, OUTPUT); 
 pinMode(yellowLED_pin, OUTPUT);
 servo.attach(servoPin);
 pid.servo = servo;
 Serial.println(startMsg);
 runStartUpLEDSequence();
 //servo.write(currentServoPosition);
} 
void loop() 
{ 
 // While there is no incoming data, the Serial available function will return a 0,
 // but when it is receiving data it will no longer be 0. So we wait to read the
 // incoming message before we handle any actions. 
 if (BT_Module.available() > 0)
 { 
   Serial.println("----\tBT BLE Msg\t----");
   handleIncomingRequest(true); 
 }
 else if (BT_ClassicModule.available() > 0)
 { 
   Serial.println("----\tBT non-BLE Msg\t----");
   handleIncomingRequest(false);  
 }
 else
 {
   digitalWrite(blueLED_pin, LOW);
   digitalWrite(redLED_pin, LOW);
   digitalWrite(yellowLED_pin, LOW); 
 }

}  

void runStartUpLEDSequence(){
  for (byte i = 0; i < 8; i++)
 {
  switch(i)
  {
    case 0:
      digitalWrite(blueLED_pin, HIGH);
      delay(500);
      break;
    case 1:
      digitalWrite(redLED_pin, HIGH);
      delay(500);
      break;
    case 2:
      digitalWrite(yellowLED_pin, HIGH);
      delay(500);
      break;
    case 3:
      digitalWrite(blueLED_pin, LOW);
      digitalWrite(redLED_pin, LOW);
      digitalWrite(yellowLED_pin, LOW);
      delay(500);
      break;
    case 4:
      digitalWrite(blueLED_pin, HIGH);
      digitalWrite(redLED_pin, HIGH);
      digitalWrite(yellowLED_pin, HIGH);
      delay(250);
      break;
    case 5:
      digitalWrite(blueLED_pin, LOW);
      digitalWrite(redLED_pin, LOW);
      digitalWrite(yellowLED_pin, LOW);
      delay(250);
      break;
    case 6:
      digitalWrite(blueLED_pin, HIGH);
      digitalWrite(redLED_pin, HIGH);
      digitalWrite(yellowLED_pin, HIGH);
      delay(250);
      break;
    case 7:
      digitalWrite(blueLED_pin, LOW);
      digitalWrite(redLED_pin, LOW);
      digitalWrite(yellowLED_pin, LOW);
      delay(250);
      break;
  }
 }
}

void handleIncomingRequest(boolean isDeviceBLE){
  Serial.println("-------------------------------------------------");
     // I believe the way the messages are being sent with the ble code, the messages
     // are being received in 4 byte array lengths. So a second loop is added to ensure
     // no dummy bytes ("0xFF") are processed.
   if(isDeviceBLE){
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
   }
   else{
     for(byte i = 0;i<8;i++){
       bt_raw_request[i] = BT_ClassicModule.read();
       Serial.print(bt_raw_request[i],HEX);
       if(i < 7)
       {
         Serial.print(":");
       }
     }
   }

   for(byte i = 0;i<8;i++){
     bt_response[i] = bt_raw_request[i];
   }
   Serial.println("");
   Serial.print("command_byte: ");
   const FullBtMsg request = btcs.Process_Request(bt_raw_request,sizeof(bt_raw_request));
   Serial.println(request.specBytes.command_byte.full_byte, HEX);
   // Serial.print("status_byte: ");
   // Serial.println(request.specBytes.status_byte.full_byte, HEX);
   
   if(btcs.isSanityCheck(request.specBytes.command_byte.full_byte)){
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
         digitalWrite(blueLED_pin,HIGH);
         bt_response[7] = 0x80;
         break;
       
       // Servo Position Sanity Check : Hex - 0x9
       case 9:
       // NOTE: When declaring variables in case instructions
       // you have to enclose all the instructions in curly braces.
       // This is because the variable has no scope without the curly braces.
       {
         Serial.println("Servo Position Sanity Check");
         byte n = 0;
         //btcs.isValidServoCommand(request.specBytes.command_byte.nibbles.lower);
         const int16_t arrayIndex = btcs.isValidServoCommand(request.specBytes.command_byte.nibbles.lower);
         if(arrayIndex != -1){
           Serial.print(btcs.ServoLookupTbl[arrayIndex].cmd, BIN);
           Serial.print(":");
           Serial.println(btcs.ServoLookupTbl[arrayIndex].pos);
           digitalWrite(yellowLED_pin,HIGH);
           runServoSanitySet(arrayIndex);
           bt_response[7] = 0x80;
         }
         else{
          digitalWrite(redLED_pin, HIGH);
          bt_response[7] = 0x60;
          Serial.println("Error : invalid servo saanity check position.");
         }
         break;
       }
       
       // Sensor Read Sanity Check : Hex - 0xA
       case 10:
         Serial.println("Sensor Read Sanity Check");
         bt_response[2] = getPosition();
         bt_response[7] = 0x80;
         break;
       
       // Tilt & Measure Sanity Check : Hex - 0xB
       case 11:
         Serial.println("Running Tilt & Measure Sanity Check");
         bt_response[7] = 0x80;
         break;
         
       default:
         Serial.println("Invalid Servo Command.");
         bt_response[7] = 0xff;
         break;
     }
     
   }
   else{
     Serial.println("This is not a sanity check");
     // checking for PID command
     unsigned long pid_StartTime = millis();
     if (request.specBytes.command_byte.nibbles.upper == 0b0100){
      // ttry to balance ffor 30 seconds (temporary limit)
      while(millis() - pid_StartTime < 30000){
        digitalWrite(blueLED_pin, HIGH);
        pid.currentBallPosition = getPosition();
        pid.runPID_control();
      }
     }
   }
   
   for(byte i = 0;i<8;i++){
     if(isDeviceBLE){
       BT_Module.write(bt_response[i]);
     }
     else{
       BT_ClassicModule.write(bt_response[i]);
     }
   }
   delay(1500);
}

void runServoSanitySet(int16_t setting){
  const byte arrLen = sizeof(btcs.ServoLookupTbl)/sizeof(btcs.ServoLookupTbl[0]);
  if (setting == arrLen-1){
    for (byte i = 0; i < 2; i++){
      for (byte n = 0; n < arrLen-1; n++){
        setServoPosition(btcs.ServoLookupTbl[n].pos);
        delay(500);
      }
    }
  } else {
    Serial.print("setting: ");
    Serial.println(setting);
    setServoPosition(btcs.ServoLookupTbl[setting].pos);
  }
}

void setServoPosition(byte pos){
  Serial.println(pos);
  if(pos <= max_angle && pos >= min_angle){
    servo.write(pos);
    delay(50); 
  }
}

unsigned int getPosition(){
 uint16_t  i = 0;
 int8_t distance = 0;
 startTime = millis();
 currentTime = startTime;
 while (currentTime - startTime < 100){
   distance += SharpIR.getDistance();
   i+=1;
   currentTime = millis();
 }
 return (unsigned int)distance/i;
}
