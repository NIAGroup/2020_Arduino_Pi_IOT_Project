import time
from bluepy import *

def sendMsg(bdaddr,msg_byte):
    print("Connecting...")
    dev = btle.Peripheral(bdaddr)
    services = list(dev.services)
    characteristic = services[len(services)-1].getCharacteristics()[0]
    characteristic.write(bytes([msg_byte]))
    print("Sending message:",msg_byte)
    dev.disconnect()
    print("Disconnected.")
    del dev

bdaddr = "00:35:FF:0D:41:9B"
msg_byte = 254
sendMsg(bdaddr,msg_byte)
