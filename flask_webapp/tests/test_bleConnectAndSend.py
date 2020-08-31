import time
from bluepy import *

# Bluetooth Low Energy communication test
# The function below sends a command to a specific ble device.
# To connect the ble device, the function will require the ble
# device's bluetooth address & the message as a byte value. The
# message will be sent byte by byte.
def sendMsg(bdaddr,msg_byte):
    print("Connecting...")
    
    # Using the bluepy library we create a "Peripheral" object with the 
    # bluetooth address. 
    # NOTE : BLE connections work as a Client (master) and 1 or more 
    # Servers (slaves)
    dev = btle.Peripheral(bdaddr)

    # BLE devices use services to handle different tasks to communicate
    # different data types (i.e. heart rate monitoring or pace makers).
    # Each service has multiple charecteristics. Below we get the correct
    # service for the HM-10 ble module on the arduino, and write it with
    # the characteristic object.
    services = list(dev.services)
    characteristic = services[len(services)-1].getCharacteristics()[0]

    # Below we actually write the message, and convert it to a byte to be
    # sent.
    characteristic.write(bytes([msg_byte]))
    print("Sending message:",msg_byte)

    # Once communication is complete, a good practice is to disconnect as
    # BLE devices are not discoverable while they are in a live connection.
    dev.disconnect()
    print("Disconnected.")
    del dev

# The Bluetooth address is usually found during the scanning process
# Because the data is sent byte by byte, each single byte that is sent
# has a value range of 0-255.
bdaddr = "00:35:FF:0D:41:9B"
msg_byte = 254
sendMsg(bdaddr,msg_byte)
