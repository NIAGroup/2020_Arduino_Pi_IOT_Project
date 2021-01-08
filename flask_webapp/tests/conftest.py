"""
File:
    conftest.py
Description:

Classes:

Author:
    Adoany Berhe
"""
import __init__
import inspect
import pytest
from src import messages
import bluetooth
from bluepy import btle

@pytest.fixture
def message_classes():
    def _msg_obj_iterator():
        for name, obj in inspect.getmembers(messages):
            if inspect.isclass(obj) and ("Message" in name):
                yield obj

    return _msg_obj_iterator()

@pytest.fixture
def message_structure_names():
    names = []
    for name, obj in inspect.getmembers(messages):
        if inspect.isclass(obj) and not("Union" in name) and ("Message" in name):
            names.append(name)
    return names

class MockBluetoothSocketConnection(object):
    @staticmethod
    def connect(*args, **kwargs): # Any arguments may be passed, it'll always return True
        print("\nConnected to Mock bluetooth object.")

    @staticmethod
    def close():
        print("Closing a connection to a Mock bluetooth object.")

@pytest.fixture
def get_mock_non_ble_connection(monkeypatch):
    def get_mock_bluetooth_socket(*args, **kwargs):
        print("\nInvoking the regular bluetooth Mock object.")
        return MockBluetoothSocketConnection()
    monkeypatch.setattr(bluetooth, "BluetoothSocket", get_mock_bluetooth_socket)

class mock_characteristic(object):
    def __init__(self):
        """
        Params of a bleio.characteristic class - per spec (https://circuitpython.readthedocs.io/en/4.x/shared-bindings/bleio/Characteristic.html#bleio.Characteristic)
        uuid (bleio.UUID) – The uuid of the characteristic
        broadcast (bool) – Allowed in advertising packets
        indicate (bool) – Server will indicate to the client when the value is set and wait for a response
        notify (bool) – Server will notify the client when the value is set
        read (bool) – Clients may read this characteristic
        write (bool) – Clients may write this characteristic; a response will be sent back
        write_no_response (bool) – Clients may write this characteristic; no response will be sent back
        """
        self.char_uuid = 0
        self.handle = 0
        self.broadcast = False
        self.indicate = False
        self.notify = False
        self.read = False
        self.write = False
        self.write_no_response = False

    def getHandle(self):
        return self.handle

class mock_service(object):
    def __init__(self):
        """
        Params bleio.Service class - per spec (https://circuitpython.readthedocs.io/en/4.x/shared-bindings/bleio/Service.html#bleio.Service)
        uuid (bleio.UUID) – The uuid of the service
        characteristics (iterable) – the Characteristic objects for this service
        secondary (bool) – If the service is a secondary one
        """
        self.ser_uuid = 0
        self.characteristics = [mock_characteristic()]

    def getCharacteristics(self):
        return self.characteristics

class MockBluetoothBlePeripheralConnection:
    def __init__(self):
        self.services = [mock_service()]
    @staticmethod
    def disconnect():
        print("Disconnecting the Mock bluetooth ble object.")

    @staticmethod
    def setDelegate(*args):
        print("Mock setDelegate api invoked.")

@pytest.fixture
def get_mock_ble_connection(monkeypatch):
    def get_mock_btle_peripheral(*args, **kwargs):
        print("\nInvoking the bluetooth ble Mock object.")
        return MockBluetoothBlePeripheralConnection()
    monkeypatch.setattr(btle, "Peripheral", get_mock_btle_peripheral)