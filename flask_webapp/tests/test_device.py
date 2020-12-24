"""
File:
    test_messages.py
Description:
    Unit test file for testing message structures and unions for size and format conformity.
Author:
    Adoany Berhe
"""
import __init__
from src.device import Bt_Ble_Device, Bt_Device

def test_ble_bt_device_initialization():
    addr = 1
    name = "test"
    ble_dev = Bt_Ble_Device(addr, name)
    assert ble_dev._addr == addr, "Device address expected to be set upon instantiating a ble device."
    assert ble_dev._name == name, "Device name expected to be set upon instantiating a ble device."
    assert ble_dev._timeout == 60, "Expected default command timeout value is 60"

def test_regular_bt_device_initialization():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Device(addr, name)
    assert bt_dev._addr == addr, "Device address expected to be set upon instantiating a ble device."
    assert bt_dev._name == name, "Device name expected to be set upon instantiating a ble device."
    assert bt_dev._timeout == 60, "Expected default command timeout value is 60. Received a different value."
    assert bt_dev._port == 1, "Expected default value of port is 1. Received a different value."
    assert bt_dev._buflen == 8, "Read buffer length is expected to be 8 bytes. Received a different value."
    port = 2
    bt_dev = Bt_Device(addr, name, port)
    assert bt_dev._port == port, "Port number expected to be set upon instantiation. Received a different value."

def test_ble_bt_device_failed_connection():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    ble_dev = Bt_Ble_Device(addr, name)
    print("\nExpecting an Exception to be raised here.")
    assert ble_dev.connect() == False, "Expected an exception to be handled and False to be returned."

def test_ble_bt_device_successful_connection(get_mock_ble_connection):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Ble_Device(addr, name)
    assert bt_dev.connect() == True, "Expected a True returned from Mock object."

def test_regular_bt_device_failed_connection():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Device(addr, name)
    print("\nExpecting an Exception to be raised here.")
    assert bt_dev.connect() == False, "Expected an exception to be handled and False to be returned."

def test_regular_bt_device_successful_connection(get_mock_non_ble_connection):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Device(addr, name)
    assert bt_dev.connect() == True, "Expected a True returned from Mock object."
    assert bt_dev._sock, "Sock (Bluetooth socket) should be set if connection is made."