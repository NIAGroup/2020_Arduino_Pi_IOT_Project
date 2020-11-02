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
#from bluepy import btle
from messages import *
#from device_delegate import BtleDelegate

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
        self._timeout = 10       # timeout value to receive a response in seconds

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
            self._delegate = BtleDelegate(self._characteristic)
            self._dev.setDelegate(BtleDelegate(self._characteristic))
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
        self._characteristic.write(msg)

    def _read(self):
        """
        Brief:

        Description:

        Return:

        """
        if self._dev.waitForNotifications(self._timeout):
            if self._delegate.response_message_data:
                print(f"Message bytes received from handle {self._delegate.response_message_characteristic}: {self._delegate.response_message_data}")
            else:
                print(f"Received bytes from an unexpected service/characteristic handle: Expected {self._delegate._characteristic} "
                      f"and received from handle {self._delegate.response_message_characteristic}")
                print("Returning None!")
        return self._delegate.response_message_data

    def send_message(self, msgName):
        """
        Brief:
            send_message(msgName): generic message sending API.
        Description:
            This function will be used to issue any request commands to a bluetooth peripheral device and parse/process
                the response message payload.
                Request command name (string) -> Response message (bytes)
        Param(s):
            msg_name: bluetooth request message name(string) to be sent to the peripheral device.
        Return:
             Response message bytes, None on failure.
        """
        import pdb; pdb.set_trace()
        msg_type = eval(f"{msgName}_Message_Union")
        msg_obj = msg_type()    # Todo: Probably need a try-except here
        msg_obj.structure.command = 0x90
        msg_bytes = msg_obj.bytes   # Todo: Figure this out
        self._write(msg_bytes)
        ret_bytes = self._read()
        if ret_bytes:
            resp_msg_union = Response_Message_Union()
            for byte_idx in range(len(resp_msg_union.bytes)):
                resp_msg_union.bytes[byte_idx] = ret_bytes[byte_idx]

            print(resp_msg_union.structure)

        return True

class Bt_Device(object):
    """

    """
    pass
