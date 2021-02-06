import time, argparse
from bluepy import *

"""
Bluetooth Low Energy communication test
The function below sends a command to a specific ble device.
To connect the ble device, the function will require the ble
device's bluetooth address & the message as a byte value. The
message will be sent byte by byte.
"""

class BtleDelegate(btle.DefaultDelegate):
    response = []
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialize here
        #print("initialized delegate")

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        #print(f"cHandle : {cHandle}, data: {data}")
        #print(list(data))
        self.response = list(data)

def sendMsg(bdaddr,msg_byte, Kp, Ki, Kd):
    print("Connecting...")
    
    """
    Using the bluepy library we create a "Peripheral" object with the 
    bluetooth address. If there is an error connecting to the provided
    bluetooth address (bdaddr), and error message will be returned. If
    connection is successful, the function will return a "Success" 
    message.

    NOTE : BLE connections work as a Client (master) and 1 or more 
    Servers (slaves)
    """
    try:
        dev = btle.Peripheral(bdaddr)

        # Attempting to set the delegate to be notified of incoming messages
        try:
            dev.setDelegate(BtleDelegate())
        except Exception:
            print("Failed to declare the delegate.")

        """
        BLE devices use services to handle different tasks to communicate
        different data types (i.e. heart rate monitoring or pace makers).
        Each service has multiple charecteristics. Below we get the correct
        service for the HM-10 ble module on the arduino, and write it with
        the characteristic object.
        """
        # test line - print("getting services")
        services = list(dev.services)
        ''' The Following block will be retained for testing purposes
        for service in services:
            print("Service: "+service.uuid.getCommonName())
            for d in service.getDescriptors():
                print(d)
            for chara in service.getCharacteristics():
                print("\t"+chara.propertiesToString())'''

        # test line - print("getting characteristics")
        characteristic = services[len(services)-1].getCharacteristics()[0]

        # Below we actually write the message, and convert it to a byte to be sent.
        #print("sending message:",msg_byte)
        if msg_byte.find("4") != -1:
            print(f"Kp : {int(Kp,16)/100}, Ki : {int(Ki,16)/100}, Kd : {int(Kd,16)/100}")
            
        full_msg = [msg_byte,"f1","f2",Kp,Ki,Kd,"f6","f7"]
        dev_name = services[0].getCharacteristics()[0].read().decode("utf-8")
        print("request:", ":".join(full_msg))
        #characteristic.write(bytes([int(full_msg,16)]))
        for b in range (0,8):
        #    full_msg = int(b,16)
            characteristic.write(bytes([int(full_msg[b],16)]))
        #characteristic.write(full_msg)
        print("-"*50)
        print(f"request sent to: {dev_name}")
        print("-"*50)

        """
        Once communication is complete, a good practice is to disconnect as
        BLE devices are not discoverable while they are in a live connection.
        """
        #dev.disconnect()
        #print("Disconnected.")
        #del dev
        
        # The following loop waits for a response from the arduino
        while True:
            if dev.waitForNotifications(1.0):
                print("notification : message received")
                print(":".join('{:02x}'.format(b) for b in dev.delegate.response ))
                break
        return "Success"

    except Exception:
        return "Failed to Connect to BLE device"
"""
In the function below, the arguments are collected and used to define the target bluetooth
devices. This is with the expectation that the file is being called as a command line 
argument. If there are no argument values, the code will default to the known working
commands. The objective of this function is to make testing easier for arduino development.

NOTE: A user can use both arguments or just one.
"""
def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bdaddr',type=str,help='Please provide an address for your bluetooth device')
    parser.add_argument('--msg',type=str,help='Please provide a byte message to be sent')
    parser.add_argument('--Kp',type=str,help='Please provide a byte message to be sent')
    parser.add_argument('--Ki',type=str,help='Please provide a byte message to be sent')
    parser.add_argument('--Kd',type=str,help='Please provide a byte message to be sent')
    args = parser.parse_args()
    bdaddr = args.bdaddr
    msg_byte = args.msg
    Kp_byte = args.Kp
    Ki_byte = args.Ki
    Kd_byte = args.Kd
    if bdaddr == None:
        bdaddr = "00:35:FF:0D:41:9B"
    if Kp_byte == None:
        Kp_byte = hex(int("00",16))
    else:
        Kp_byte = hex(int(Kp_byte,16))
    if Ki_byte == None:
        Ki_byte = hex(int("00",16))
    else:
        Ki_byte = hex(int(Ki_byte,16))
    if Kd_byte == None:
        Kd_byte = hex(int("00",16))
    else:
        Kd_byte = hex(int(Kd_byte,16))
    if msg_byte == None:
        msg_byte = hex(int("90",16))   # sets the servo to 90 degrees
    else:
        msg_byte = hex(int(msg_byte,16))
    return bdaddr,msg_byte, Kp_byte, Ki_byte, Kd_byte

"""
The Bluetooth address is usually found during the scanning process
Because the data is sent byte by byte, each single byte that is sent
has a value range of 0-255.

The arguments passed in will be checked for the correct formatting as well,
but this will have to be updated later to match the communication standard
for an array of bytes.
"""
bdaddr, msg_byte, Kp, Ki, Kd = getArguments()
print(msg_byte)

if (int(msg_byte,16) > 0 and int(msg_byte,16) < 256):
    if bdaddr.count(":") == 5 and len(bdaddr) == 17:
        print(f"bdaddr : {bdaddr}")
        print(f"msg_byte : {msg_byte}")
        status = sendMsg(bdaddr,msg_byte, Kp, Ki, Kd)
        print(status)
    else:
        print("The bluetooth address is not formatted correctly.\nPlease try again following syntax 'xx:xx:xx:xx:xx:xx'")
else:
    print("The message byte must be between 0 and 255.\nPlease provide a valid message byte value.")
