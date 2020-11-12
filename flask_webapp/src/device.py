"""
File:
    device.py
Description:
    Describes bluetooth device abstractions for define read, write, scan, connect APIs.
Classes:
    Bt_Ble_Device, Bt_Device
Author:
    Adoany Berhe, Princton Brennan
"""
import __init__
from bluepy import btle
from messages import *
from device_delegate import BtleDelegate

class Bt_Ble_Device(object):
    """
    Brief:
        Bt_Ble_Device(): abstraction class for a bluetooth ble device
    Description:
        This class contains all the APIs a bluetooth connected LE device needs to implement.
    Methods:
        connect, send_message, _write, _read
    """
    def __init__(self, addr):
        """
        Brief:
            __init__(addr): Initializer to Bt_Ble_Device.
        Param(s):
            addr: address of the device.
        """
        self._addr = addr
        self._timeout = 60       # timeout value to receive a response in seconds

    def connect(self):
        """
        Brief:
            connect(): Connect API for bluetooth ble API.
        Return:
            True upon successfully connecting/paring; False upon unexpected errors.
        """
        try:
            self._dev = btle.Peripheral(self._addr)
            self._services = list(self._dev.services)
            self._characteristic = self._services[len(self._services) - 1].getCharacteristics()[0]
            self._delegate = BtleDelegate(self._characteristic.getHandle())
            self._dev.setDelegate(self._delegate)
        except Exception:
            print(f"Unexpected Error occurred upon connecting.\n {Exception}")
            return False
        return True

    def __del__(self):
        """
        Brief:
            __del__(): Custom destructor API for the instance
        Description:
            This method first disconnects the bluetooth device then deletes ble peripheral device.
        """
        self._dev.disconnect()
        del self._dev

    def _write(self, msg):
        """
        Brief:

        Description:

        Param(s):
            msg:

        """
        msg.bytes[1] = 241
        msg.bytes[2] = 242
        msg.bytes[3] = 243
        msg.bytes[4] = 244
        msg.bytes[5] = 245
        msg.bytes[6] = 246
        msg.bytes[7] = 247  
        print(f"About to perform a write with bytes: {bytearray(msg.bytes)}\n")      
        for a_byte in msg.bytes:
            #print("I'm about to write the following:")
            #print(bytes([a_byte])) 
            self._characteristic.write(bytes([a_byte]))

    def _read(self):
        """
        Brief:

        Description:

        Return:

        """
        try:
            if self._dev.waitForNotifications(self._timeout):
                if self._delegate.response_message_data:
                    print(f"Message bytes received from handle {self._delegate.response_message_handle}: {self._delegate.response_message_data}\n")
                else:
                    print(f"Received bytes from an unexpected service/characteristic handle: Expected {self._delegate._char_handle} "
                      f"and received from handle {self._delegate.response_message_handle}")
                    print("Returning None!")
        except btle.BTLEDisconnectError as error:
            print(f"An error occured upon reading response. \n{error}")
        
        return self._delegate.response_message_data

    def send_message(self, msgName, **kwargs):
        """
        Brief:
            send_message(msgName, **kwargs): generic message sending API.
        Description:
            This function will be used to issue any request commands to a bluetooth peripheral device and parse/process
                the response message payload.
                Request command name (string) -> Response message (bytes)
        Param(s):
            msg_name: bluetooth request message name(string) to be sent to the peripheral device.
        Return:
             Response message bytes, None on failure.
        """
        STATUS_SUCCESS = 0
        msg_type = eval(f"{msgName}_Message_Union")
        try:
            msg_obj = msg_type()
        except TypeError:
            print(f"Message object {msg_type} not defined. Returning False.\n{TypeError}")
            return False
        for elt_name, elt_val in kwargs.item():
            msg_obj.structure.elt_name = elt_val
        #msg_obj.structure.command = 0x90
        print(f"Writing message: {msgName}. \n{msg_obj.structure}")
        self._write(msg_obj)

        ret_bytes = self._read()
        if ret_bytes:
            resp_msg_union = Response_Message_Union()
            if len(ret_bytes) >= sizeof(resp_msg_union):
                for byte_idx in range(len(resp_msg_union.bytes)):
                    resp_msg_union.bytes[byte_idx] = ret_bytes[byte_idx]
                print(f"Received Packet: \n{resp_msg_union.structure}")
                return resp_msg_union.structure.status == STATUS_SUCCESS
            else:
                print(f"Received less bytes than expected for message: {msgName}.\n"
                      f"Expected: {sizeof(resp_msg_union)} Received: {len(ret_bytes)}. Returning False")
        else:
            print("Didn't receive any bytes from device. Returning False.")
        return False

class Bt_Device(object):
    """

    """
    pass
