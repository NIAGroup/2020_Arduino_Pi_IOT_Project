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

// Using the SoftwareSerial Library, the Digital IO pins 2 & 3 are repurposed as Soft Serial Pins
// NOTE : For wiring the TX pin of the target device/module is connected to the assigned RX pin of the
// Microcontroller, and the RX pin of the target device/module is connected to the assigned TX pin of
// the Microcontroller.  
SoftwareSerial BT_Module(2, 3); // assigned RX , assigned TX 
char bt_msg;    // The bluetooth messagge will be received one byte a time, which can be represented as a character (char) 
int LED = 11;   // The LED pin assigned to pin 11.

// Every Arduino sketch requires at least a setup loop for initializing I/O pins and serial ports
// and a main function called "loop" that will loop indefinitely while the board is powered.
void setup() 
{   
 Serial.begin(38400);       // The default baudrate for the HC-05 is 38400.  
 BT_Module.begin(38400);       // If the baudrate is incorrect the messages will not be read/displayed correctly.
 pinMode(LED, OUTPUT);      // The led pin gets setup as an output pin. 
 Serial.println("Ready to connect\nDefualt password is 1234 or 000"); 
} 
void loop() 
{ 
 // While there is no incoming data, the Serial available function will return a 0,
 // but when it is receiving data it will no longer be 0. So we wait to read the
 // incoming message before we handle any actions. 
 if (BT_Module.available() > 0)
 { 
     readBT_Msg();
 }

}  

void readBT_Msg(){
    bt_msg = BT_Module.read();      // Here we read the incoming message as a byte represented as a char
  Serial.println(bt_msg);         // The incoming message will be printed in the Arduino IDE Serial Monitor -  CTRL+SHIFT+M
  
  // If the message is a 1, the LED will be turned on.
  if (bt_msg == '1') 
   { 
     digitalWrite(LED, HIGH); 
     Serial.println("LED On"); 
   }
   // If the message is a 0, the LED will be turned off. 
   else if (bt_msg == '0') 
   { 
     digitalWrite(LED, LOW); 
     Serial.println("LED Off"); 
   } 
}

