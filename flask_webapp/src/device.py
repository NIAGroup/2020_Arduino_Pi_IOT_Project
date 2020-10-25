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

    """
    def __init__(self, addr):
        """
        Brief:
            __init__(addr): Initializer to Bt_Ble_Device.
        Param(s):
            addr: address of the device.
        """
        self._addr = addr

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
            __del__(): Custom delete API
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
        retVal = None
        while True:
            if self._dev.waitForNotifications(1.0):
                if self._delegate.response:
                    print(f"Read message received: {self._delegate.response}")
                    retVal = self._delegate.response
                    break
        return retVal

    def send_message(self, msgName):
        """
        Brief:

        Description:

        Param(s):

        Return:

        """
        msg_type = eval(f"{msgName}_Message")
        msg_obj = msg_type()    # Todo: Probably need a try-except here
        msg_bytes = msg_obj.bytes()  # Todo: Figure this out
        self._write(msg_bytes)
        self._read()
        return True

class Bt_Device(object):
    """

    """
    pass
