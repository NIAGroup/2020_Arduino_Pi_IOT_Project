#include <SharpIR.h>
SharpIR SharpIR( SharpIR::GP2Y0A21YK0F, A0 );

unsigned long eventInterval = 250;
unsigned int previousDistance;
unsigned int currentDistance;
unsigned long previousTime = 0;
unsigned long currentTime = millis();

String startMsg = "################################\n" \
                  "      running Sensor Example    \n" \
                  "################################";


void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600); 
 delay(500);
 Serial.println(startMsg);
}

void loop() {
  // put your main code here, to run repeatedly:
  //getSensorReading(millis());
  Serial.print(SharpIR.getDistance());
  Serial.print("\t\t");
  Serial.println(SharpIR.getDistance() * 2.54);
  delay(100);
}

void getSensorReading(unsigned long startTime){
 int  i = 0;
 int distance = 0;
 currentTime = startTime;
 while (currentTime - startTime < eventInterval){
   distance += SharpIR.getDistance() * 2.54;
   Serial.print("\t\t");
   Serial.println(SharpIR.getDistance());
   Serial.print("\t\t");
   Serial.println(SharpIR.getDistance() * 2.54);
   i+=1;
   currentTime = millis();
 }
   
   Serial.print("Distance: ");
   Serial.print(distance/i);
   Serial.println("cm");
}
