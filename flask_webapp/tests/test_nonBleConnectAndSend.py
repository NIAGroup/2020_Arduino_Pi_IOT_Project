#!/usr/bin/env python3
"""PyBluez simple example rfcomm-client.py
Simple demonstration of a client application that uses RFCOMM sockets intended
for use with rfcomm-server.
Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $
"""
import time, argparse, sys, bluetooth

def sendMsg(bdaddr,msg_byte):
    print("Connecting...")
    # Create the client socket
    try:
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((bdaddr, port))
        print("Connected!")
        full_msg = [msg_byte,"f1","f2","f3","f4","f5","f6","f7"]
        full_msg = [msg_byte,"00","00","00","00","00","00","00"]
        #print(dir(sock))
        print("request:", ":".join(full_msg))
        print("-"*50)
        print(f"request sent to: {bluetooth.lookup_name(bdaddr)}")
        print("-"*50)
        for b in range (0,8): 
            sock.send(bytes([int(full_msg[b],16)]))
        response = []
        sock.setblocking(0)
        time.sleep(1)
        sock.setblocking(1)
        while True:
            data = sock.recv(8)
            for b in data:
                #print(hex(b))
                response.append(b)
            if(len(response) > 7 or len(response) == 8):
                break
        data = ":".join('{:02x}'.format(b) for b in response)
        print("notification : message received")
        print(f"{data}")
        sock.close()
        time.sleep(1)
        return "Success"
    except Exception:
        return "Failure to Connect"
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
    args = parser.parse_args()
    bdaddr = args.bdaddr
    msg_byte = args.msg
    if bdaddr == None:
        bdaddr = "00:14:03:06:12:84"
    if msg_byte == None:
        msg_byte = hex(int("90",16))   # sets the servo to 90 degrees
    else:
        msg_byte = hex(int(msg_byte,16))
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
print(msg_byte)

if (int(msg_byte,16) >= 0 and int(msg_byte,16) < 256):
    if bdaddr.count(":") == 5 and len(bdaddr) == 17:
        print(f"bdaddr : {bdaddr}")
        print(f"msg_byte : {msg_byte}")
        status = sendMsg(bdaddr,msg_byte)
        print(status)
    else:
        print("The bluetooth address is not formatted correctly.\nPlease try again following syntax 'xx:xx:xx:xx:xx:xx'")
else:
    print("The message byte must be from 0 to 255.\nPlease provide a valid message byte value.")
