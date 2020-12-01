#include <Servo.h>
#include <SharpIR.h>

#define IR A0 // define signal pin
#define model 1080 // used 1080 because model GP2Y0A21YK0F is used
SharpIR SharpIR(IR, model);

const byte servoPin = 6;    // Servo pin assigned as pin 6 [servos require a PWM pin].
Servo servo;           

unsigned long eventInterval = 1000;
unsigned long previousTime = 0;
unsigned long currentTime = millis();
String startMsg = "################################\n" \
                  "  running Servo/Sensor Example  \n" \
                  "################################";

void setup(){
 Serial.begin(9600); 
 servo.attach(servoPin);
 servo.write(30);
 Serial.print(startMsg);
 //eventInterval = 2000;
 //runTimer(millis());
}

void loop(){
  if (Serial.available() > 0){
    char x = Serial.read();
    switch (x){
     case '1':
       servo.write(0);
       runTimer(millis());
       break;
     case '2':
       servo.write(30);
       runTimer(millis());
       break;
     case '3':
       servo.write(60);
       runTimer(millis());
       break;
     case '4':
       servo.write(90);
       runTimer(millis());
       break;
     case '5':
       servo.write(120);
       runTimer(millis());
       break;
     case '6':
       servo.write(150);
       runTimer(millis());
       break;
     case '7':
       servo.write(180);
       runTimer(millis());
       break;
    }
  }
 //SeeSawFxn();
}

void SeeSawFxn(){
  byte pos = 0;
  for (pos = 0; pos < 180; pos+=5){
    servo.write(pos);
    delay(100);
  } 
  for (pos = 180; pos > 0; pos-=5){
    servo.write(pos);
    delay(100);
  }
}



void runTimer(unsigned long startTime){
 int  i = 0;
 int distance = 0;
 currentTime = startTime;
 while (currentTime - startTime < eventInterval){
   /*Serial.print("currentTime:");
   Serial.print(currentTime);
   Serial.print(", Delta: ");
   Serial.println(currentTime - startTime);*/
   distance += SharpIR.distance();
   i+=1;
   currentTime = millis();
 }
   
   Serial.print("\nDistance: ");
   Serial.print(distance/i);
   Serial.println("cm");
   Serial.print("start time: "); 
   Serial.print(startTime); 
   Serial.print(", current time: "); 
   Serial.print(currentTime);
   Serial.print(", previous time: ");
   Serial.println(previousTime);
}
