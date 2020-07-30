
# Arduino PID Cotroller - Ball Balance

_PID Controller - A proportional–integral–derivative controller (PID controller or three-term controller) is a control loop mechanism employing feedback that is widely used in industrial control systems and a variety of other applications requiring continuously modulated control._

![PID Controller - Control Systems Illustration](https://github.com/NIAGroup/2020_Arduino_Pi_IOT_Project/blob/master/arduino_pid_controller/img/PID-control_illustration.jpg)

![PID Controller - Equation](https://github.com/NIAGroup/2020_Arduino_Pi_IOT_Project/blob/master/arduino_pid_controller/img/pid_controller_equation.png)

![Balance Apparatus Example](https://github.com/NIAGroup/2020_Arduino_Pi_IOT_Project/blob/master/arduino_pid_controller/img/PID_Balance_Example_Apparatus.jpg)

#### Objective - _To balance a ping-pong ball in the center of a beam using an arduino & communicating the results to a raspberry pi via a Bluetooth connection_ 

### Control System Breakdown
* P [Process] - The Ping-Pong Ball position
* S<sub>p</sub> [Setpoint position] - Arduino programmed desired middle position
* F<sub>p</sub> [Feedback position] - Ultrasonic Distance Sensor real position based on distance reading
* E [Error]- E = S<sub>p</sub> - F<sub>p</sub>
> NOTE : Error is the difference between the desired ping-pong ball position (S<sub>p</sub>) and the actual ping-pong ball position measured by the sensor (F<sub>p</sub>).
* PID_p = K<sub>p</sub> * E
* PID_i = PID_i + K<sub>i</sub> * E
> NOTE : The integral is based on the sum of error over time. So at t<sub>0</sub> the will be the integral constanct * the error, but this will grow and decrease gradually over time as the error changes.
* PID_d = K<sub>d</sub> * (E<sub>c</sub> - E<sub>p</sub> /Δt)
> NOTE : For the derivitave calculation we consider the ping-pong ball velocity. Which is the change in position (displacement) divided by the change in time. `Δx/Δt`, where Δx is the current Error (E<sub>c</sub>) - the previous error (E<sub>p</sub>). 

### Major Components
* Arduino Uno 
* HC-05 Bluetooth Module
* Sg90 Micro Servo
* Ultrasonic Distance Sensor

### Desired features
1. The Arduino should be able to provide the position of the ping-pong ball by reading the ultrasonic distance sensor.
2. The Arduino should be able to actuate the servo to pivot a balance beam left and right quickly.
3. The Arduino should be able to both receive commands from a raspberry pi & return results over a bluetooth connection using the hc-05 bluetooth module.
> NOTE: The main result would be the time needed to balance the ping-pong ball.
4. The Control System should be able to balance the ping-pong ball from any starting point of the ping-pong ball along the balance beam and from any starting position of the balance beam (i.e. starting at an angle that is not 0 degrees; parallel to the base).
5. The Control System should be able to accept PID parameter values (K<sub>p</sub>, K<sub>i</sub>, K<sub>d</sub>) sent to it from the Raspberry Pi. 
6. Upon power up, the balance beam should have a default start position. 
7. The Arduino should be able to set specific balance beam position/angles to start at (i.e. -20 degrees or 30 degrees).
8. The Arduino should have a general response message for verifying bluetooth communication with the Raspberry Pi. (i.e. Pi sends: "?", Arduino response: "!")
