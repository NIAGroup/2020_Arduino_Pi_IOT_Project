/*
 * Author :  Princton Brennan, Injoh M. Tanwani
 * Date:  09-20-20
 * Purpose : Beginner's Example for sensor reading & PWM writing 
 * Requirements : 1 LED, Ultrasonic Distance Sensor (model - HC-SR04), & an Arduino   
 * 
 * Function : The sensor will be used to measure an object's distance (your hand works fine) 
 * in inches and centimeters and adjusts the intensity of an LED based on that distance. 
 * The LED will increase it's intensity as the object gets closer, and adversely decrease as
 * the object moves further away. The distance & intensity values will be visible in the
 * arduino ide serial monitor. 
 * 
 * NOTE :: Most LED's that come in kits are rated for 3V, so to be safe the maximum equivalent voltage  
 * that will be written to set the LED's intensity will be 2.5V. 
 * 
 * NOTE :: This original code was written to work with the Arduino Mega, Uno, & Nano boards
 * as they provide a 5V supply pin. This is needed to power the sensor. 
 * 
 */


// For good practice to not waste memory, smaller variable types are used when possible 
// (e.g. using byte (8 bit length) instead of an int (32bit length)
// Additionally, constants are used for values that will not change.   
const byte ledPin =  11;          // The LED pin assigned to pin 11. (Be sure that this is a PWM pin on your board by reviewing your board's pinout).
byte led_intensity_val;           // The maximum value of a byte is 255, which translates to the maximum output voltage for PWM 

unsigned long time;
unsigned long prev;
unsigned long curr;
unsigned long DELAY_TIME = 10000; // 10 sec
unsigned long delayStart = 0; // the time the delay started
bool delayRunning = false; // true if still waiting for delay to finish


/*
 * The variables below will be used for controlling the HC-SR04 Ultrasonic Sensor
 * It will require 2 digital pins: trigger & echo
 * Both must be used to send the ultrasonic signal, and another is used to capture
 * the signal once it returns. The distance will be calculated for inches & centimeters
 * NOTE: These values can be adjusted
 * 
 * For more information about how the sensor works : https://randomnerdtutorials.com/complete-guide-for-ultrasonic-sensor-hc-sr04/
*/      
const byte trigPin = 4;         // Trigger pin assigned to pin 4. 
const byte echoPin = 5;         // Echo pin assigned to pin 5.

long duration;
float distance_in_centimeters, distance_in_inches;

// Every Arduino sketch requires at least a setup loop for initializing I/O pins and serial ports
// and a main function called "loop" that will loop indefinitely while the board is powered.
void setup() {
  // The default baudrate for the Serial Port is 9600 for the Serial Monitor output, but it can be changed to
  // fit the needs of your project.
  Serial.begin (9600);
  pinMode(ledPin, OUTPUT);        // The led pin gets setup as an output pin.
  pinMode(trigPin, OUTPUT);       // The trigger pin gets setup as an output pin.
  pinMode(echoPin, INPUT);        // The echo pin (sensor output signal) gets setup as an output pin.
}

void loop() {
  ultrasonicRead();       // To keep the main loop easy to read, all operation specific functions are written seperately.
  Time();
  
}

void ultrasonicRead()
{
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //start delay
  delayStart = millis();
  delayRunning = true;

  
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
 
  // Convert the time into a distance
  distance_in_centimeters = (duration/2) / 29.1;      // Divide by 29.1 or multiply by 0.0343
  distance_in_inches = (duration/2) / 74;             // Divide by 74 or multiply by 0.0135

  // The distance measured is being limited to 2cm-35m, so the results are only being printed
  // for distances within that range. The includes adjustments to the LED intensity as well.
  if (distance_in_centimeters > 2 && distance_in_centimeters < 35)

  {
    Serial.print(distance_in_inches);
    Serial.print("in, ");
    Serial.print(distance_in_centimeters);
    Serial.print("cm");
    
    // The map function is a builtin function to simplify linearly related ranges. The led 
    // intensity will be mapped to a range from 0-128 based on our distance measurement range
    // of 5-20cm. Our mapping is the inverse: i.e. minimum distance = maximum led intensity
    // while the maximum distance = minimum led intensity.
    // syntax: [value to be mapped] = map([value to read/compare], [min read value], [max read value], [min write value], [max write value])
    //
    // For this example it was adjusted to be the inverse:
    // [value to be mapped] = map([value to read/compare], [min read value], [max read value], [max write value], [min write value])
    led_intensity_val = map(distance_in_centimeters, 5, 30, 128 , 0);
    Serial.print(", led intensity: ");
    Serial.print(led_intensity_val);
    Serial.println();
    analogWrite(ledPin,led_intensity_val);
    Serial.println();
    Serial.println();

  }

  // If we're not within our set ditance range, we'll simply print out a warning message.
  else{
    Serial.println("Too far or too close. Please adjust your distance...");
  }
  delay(100);
}

void Time()
{
  const byte eventInterval = 1000;
  unsigned long previousTime = 0;
  unsigned long currentTime = millis();
 
  if(currentTime - previousTime >= eventInterval) {

     for( byte i = 0; i <=10; i++)
     { 
       Serial.print("Minutes: ");
       Serial.println(i);
       Serial.println();
     }
    
     previousTime = currentTime;
  }
 
}
