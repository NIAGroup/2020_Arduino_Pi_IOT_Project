"""
File:
    test_messages.py
Description:
    Unit test file for testing message structures and unions for size and format conformity.
Author:
    Adoany Berhe
"""
import __init__
from src import device
from src.device import *

def test_ble_bt_device_initialization():
    addr = 1
    name = "test"
    ble_dev = Bt_Ble_Device(addr, name)
    assert ble_dev._addr == addr, "Device address expected to be set upon instantiating a ble device."
    assert ble_dev._name == name, "Device name expected to be set upon instantiating a ble device."
    assert ble_dev._timeout == 60, "Expected default command timeout value is 60"

def test_regular_bt_device_initialization():
    addr = 1
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
