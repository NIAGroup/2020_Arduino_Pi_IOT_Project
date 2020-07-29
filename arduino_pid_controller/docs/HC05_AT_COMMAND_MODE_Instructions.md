# HC05 AT COMMAND MODE Instructions
> AT command mode allows you to write directly to the Bluetooth module and either the current settings or change some of the settings; things like the name, the baud rate, whether or not it operates in slave mode or master mode.

### HC-05 Default Settings 
* Baudrate : 38400
* Pairing Pin : 1234

> NOTE : The baud rate is the rate at which information is transferred in a communication channel. Baud rate is commonly used when discussing electronics that use serial communication. In the serial port context, "9600 baud" means that the serial port is capable of transferring a maximum of 9600 bits per second.

### Starting AT COMMAND Mode  

1. Create an "empty sketch" in your Arduino IDE or the Arduino Web Editor; here's an example:
```arduino
void setup()
{

}

void loop()
{

}

```

2. Connect the arduino to your laptop/desktop via the USB connection and upload the empty sketch to the arduino, then disconnect the USB to power down the Arduino.

3. User jumper wires to connect the arduino and hc-05 bt module according to the diagram below:
![AT Command Mode Wiring Diagram](https://github.com/NIAGroup/2020_Arduino_Pi_IOT_Project/blob/master/arduino_pid_controller/img/AT_CommandMode_Wiring_Diagram.png)

4. Disconnect the VCC jumper from the hc-05 bt module, then connect the arduino back up to the laptop/desktop via the USB cable.

5. Start the Serial Monitor (_CTRL+SHIFT+M_), or navigate to it in the Arduino Web Editor, and set the baudrate to 38400.
> Note : 38400 is the factory default baudrate for the hc-05.

6. Reconnect the VCC jumper to the hc-05 bt module. If the LED on the hc-05 begins a slow flash (roughly 2 second intervals), the module should now be in AT Command Mode.

7. Type in `AT` in the Serial Monitor terminal and hit ENTER. If the connections are correct, the module should respond with an `OK` response.

### Available AT Commands

Most useful AT commands are

* `AT` : Ceck the connection.
* `AT+NAME` : See default name
> NOTE : To change the Name, or any other settings, follow the command with an "=[the_new_value]" e.g. `AT+NAME=MyArduino01`
* `AT+ADDR` : see default address
* `AT+VERSION` : See version
* `AT+UART` : See baudrate
* `AT+ROLE`: See role of bt module(1=master/0=slave)
* `AT+RESET` : Reset and exit AT mode
* `AT+ORGL` : Restore factory settings
* `AT+PSWD` : see default password

