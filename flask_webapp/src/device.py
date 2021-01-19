"""
File:
    device.py
Description:
    Describes bluetooth device abstractions for define read, write, scan, connect APIs.
Classes:
    Bt_Ble_Device, Bt_Device
Spec:
    https://circuitpython.readthedocs.io/en/4.x/shared-bindings/bleio/__init__.html
    https://ianharvey.github.io/bluepy-doc/peripheral.html
Author:
    Adonay Berhe
"""
import __init__
import bluetooth
import socket

from bluepy import btle
from device_delegate import BtleDelegate
from messages import *

class Bt_Ble_Device(object):
    """
    Brief:
        Bt_Ble_Device(): abstraction class for a bluetooth ble device
    Description:
        This class contains all the APIs a bluetooth connected LE device needs to implement.
    Methods:
        connect, send_message, _write, _read
    """
    def __init__(self, addr, name):
        """
        Brief:
            __init__(addr): Initializer to Bt_Ble_Device.
        Param(s):
            addr: address of the device.
        """
        self._addr = addr
        self._name = name
        self._timeout = 60      # timeout value to receive a response in seconds
        self._dev = None

    @property
    def name(self):
        """
        Brief:
            name(): Getter api for _name attribute
        return:
            string (_name attribute)
        """
        return self._name

    def connect(self):
        """
        Brief:
            connect(): Connect API for bluetooth ble device.
        Return:
            True upon successfully connecting/paring; False upon unexpected errors.
        """
        try:
            self._dev = btle.Peripheral(self._addr)
            self._services = list(self._dev.services)
            self._characteristic = self._services[len(self._services) - 1].getCharacteristics()[0]
            self._delegate = BtleDelegate(self._characteristic.getHandle())
            self._dev.setDelegate(self._delegate)
        except Exception as error:
            print(f"Unexpected Error occurred upon connecting.\n{error}")
            return False
        return True

    def is_connected(self):
        """
        Brief:
            is_connected(): An API to check if bluetooth ble device is connected.
        Description:
            This method returns the btle.Peripheral built-in field 'connected'
        Return:
             True if device is still connected, False if disconnected.
        """
        return self._dev.connected

    def __del__(self):
        """
        Brief:
            __del__(): Custom destructor API for the instance
        Description:
            This method first disconnects the bluetooth device then deletes ble peripheral device.
        """
        if hasattr(self, "_dev"):
            self.disconnect()
            del self._dev

    def disconnect(self):
        """
        Brief:
            disconnect(): Disconnect API for a bluetooth ble device.
        Description:
            This API checks if a connection exists. If so it will disconnect, else it will return.
        """
        if self.is_connected():
            self._dev.disconnect()

    def _write(self, msg):
        """
        Brief:
            _write(msg): A write API for sending message bytes
        Param(s):
            msg: bytes to be sent to a bluetooth peripheral device.
        """
        print(f"About to perform a write with bytes: {bytearray(msg.bytes)}\n")      
        for a_byte in msg.bytes:
            self._characteristic.write(bytes([a_byte]))

    def _read(self):
        """
        Brief:
            _read(): Read API for obtaining response bytes from a bluetooth device.
        Return:
            Return received bytes (8-bytes) on success or None on exception
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
            msg_name: bluetooth request message name(string) to be sent to the peripheral device. '__Message_Union' is
                appended to this name before searching messages.py module for packet/structure definition.
        Return:
             Response message bytes, None on failure (NameError or any other type of Exception raised).
        """
        if self.is_connected():
            STATUS_SUCCESS = 0x00
            try:
                msg_type = eval(f"{msgName}_Message_Union")
                msg_obj = msg_type()
            except NameError as error:
                print(f"Message object {msgName} not defined. Returning False.\n{error}")
                return False

            if kwargs:
                for elt_name, elt_val in kwargs.items():
                    if hasattr(msg_obj.structure, elt_name): # only overwrite value if field is present
                        setattr(msg_obj.structure, elt_name, elt_val)

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
        else:
            print(f"\nConnection to {self._name}:{self._addr} is disconnected. Returning False")
        return False

class Bt_Device(object):
    """
    Brief:
        Bt_Device(): abstraction class for a bluetooth device
    Description:
        This class contains all the APIs a bluetooth connected device needs to implement.
    Methods:
        connect, send_message, _write, _read
    """
    def __init__(self, addr, name, port=1):
        """
        Brief:
            __init__(addr, name, port): Initializer to Bluetooth Device.
        Param(s):
            addr: address of the device.
            name: device name
            port: (defaults to 1). The port ID for bluetooth IO.
        """
        self._port = port
        self._addr = addr
        self._name = name
        self._timeout = 60  # timeout value to receive a response in seconds
        self._buflen = 8    # 8 bytes received per message

    @property
    def name(self):
        """
        Brief:
            name(): Getter api for _name attribute
        return:
            string (_name attribute)
        """
        return self._name

    def connect(self):
        """
        Brief:
            connect(): Connect API for bluetooth device.
        Return:
            True upon successfully connecting/paring; False upon unexpected errors.
        """
        try:
            self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self._sock.connect((self._addr, self._port))
            print("Connected!")
        except Exception as error:
            print(f"Unexpected Error occurred upon connecting.\n{error}")
            return False
        return True

    def is_connected(self):
        """
        Brief:
            is_connected(): An API to check if bluetooth device is connected.
        Description:
            This method invokes 'socket.getpeername' API. This API (which is inherited from python's socket class)
                returns the remote address to which the socket is connected. If not connected, it raises an error.
        Return:
             True if device is still connected, False if disconnected i.e. Exception is thrown.
        """
        try:
            self._sock.getpeername()
            return True
        except Exception as error:
            print(error)
            return False

    def __del__(self):
        """
        Brief:
            __del__(): Custom destructor API for a bluetooth client device instance
        Description:
            This method closes a bluetooth socket.
        """
        if hasattr(self, "_sock"):
            self.disconnect()
            del self._sock

    def disconnect(self):
        """
        Brief:
            disconnect(): Disconnect API for a bluetooth device.
        Description:
            This API checks if a connection exists. If so it will disconnect, else it will return.
        """
        if self.is_connected():
            self._sock.close()

    def _write(self, msg):
        """
        Brief:
            _write(msg): A write API for sending message bytes
        Param(s):
            msg: bytes to be sent to a bluetooth client device.
        """
        print(f"About to perform a write with bytes: {bytearray(msg.bytes)}\n")
        for a_byte in msg.bytes:
            self._sock.send(bytes([a_byte]))

    def _read(self):
        """
        Brief:
            _read(): Read API for obtaining response bytes from a bluetooth device.
        Return:
            Return received bytes (8-bytes) on success or None on exception
        """
        data = None
        try:
            self._sock.settimeout(self._timeout)
            data = self._sock.recv(self._buflen)
            print(f"Message bytes received: {data}\n")
        except socket.timeout as error:
            print(f"Did not receive a response package in the expected time({self._timeout}). \n{error}")

        return data

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
        if self.is_connected():
            STATUS_SUCCESS = 0x00
            try:
                msg_type = eval(f"{msgName}_Message_Union")
                msg_obj = msg_type()
            except NameError as error:
                print(f"Message object {msgName} not defined. Returning False.\n{error}")
                return False

            if kwargs:
                for elt_name, elt_val in kwargs.items():
                    if hasattr(msg_obj.structure, elt_name):  # only overwrite value if field is present
                        setattr(msg_obj.structure, elt_name, elt_val)

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
        else:
            print(f"\nConnection to {self._name}:{self._addr} is disconnected. Returning False")
        return False
