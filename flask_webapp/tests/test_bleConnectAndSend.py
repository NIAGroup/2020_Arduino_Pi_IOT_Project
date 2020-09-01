import time, argparse
from bluepy import *

"""
Bluetooth Low Energy communication test
The function below sends a command to a specific ble device.
To connect the ble device, the function will require the ble
device's bluetooth address & the message as a byte value. The
message will be sent byte by byte.
"""
def sendMsg(bdaddr,msg_byte):
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

        """
        BLE devices use services to handle different tasks to communicate
        different data types (i.e. heart rate monitoring or pace makers).
        Each service has multiple charecteristics. Below we get the correct
        service for the HM-10 ble module on the arduino, and write it with
        the characteristic object.
        """
        services = list(dev.services)
        characteristic = services[len(services)-1].getCharacteristics()[0]

        # Below we actually write the message, and convert it to a byte to be sent.
        characteristic.write(bytes([msg_byte]))
        print("Sending message:",msg_byte)

        """
        Once communication is complete, a good practice is to disconnect as
        BLE devices are not discoverable while they are in a live connection.
        """
        dev.disconnect()
        print("Disconnected.")
        del dev
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
    parser.add_argument('--msg',type=int,help='Please provide a byte message to be sent')
    args = parser.parse_args()
    bdaddr = args.bdaddr
    msg_byte = args.msg
    if bdaddr == None:
        bdaddr = "00:35:FF:0D:41:9B"
    if msg_byte == None:
        msg_byte = 254
    else:
        msg_byte = msg_byte
    return bdaddr,msg_byte

"""
The Bluetooth address is usually found during the scanning process
Because the data is sent byte by byte, each single byte that is sent
has a value range of 0-255.

The arguments passed in will be checked for the correct formatting as well,
but this will have to be updated later to match the communication standard
for an array of bytes.
"""
bdaddr, msg_byte = getArguments()
if (msg_byte > -1 and msg_byte < 256):
    if bdaddr.count(":") == 5 and len(bdaddr) == 17:
        print(f"bdaddr : {bdaddr}")
        print(f"msg_byte : {msg_byte}")
        status = sendMsg(bdaddr,msg_byte)
        print(status)
    else:
        print("The bluetooth address is not formatted correctly.\nPlease try again following syntax 'xx:xx:xx:xx:xx:xx'")
else:
    print("The message byte must be between 0 and 255.\nPlease provide a valid message byte value.")
