"""
File:
    test_messages.py
Description:
    Unit test file for testing message structures and unions for size and format conformity.
Author:
    Adoany Berhe
"""
import __init__
from unittest.mock import Mock, MagicMock
from src.messages import Response_Message_Union
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

def test_regular_bt_device_failed_connection():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Device(addr, name)
    print("\nExpecting an Exception to be raised here.")
    assert bt_dev.connect() == False, "Expected an exception to be handled and False to be returned."

def test_ble_bt_device_successful_connection(get_mock_ble_connection):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    ble_dev = Bt_Ble_Device(addr, name)
    assert ble_dev.connect() == True, "Expected a True returned from Mock object."

def test_regular_bt_device_successful_connection(get_mock_non_ble_connection):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    bt_dev = Bt_Device(addr, name)
    assert bt_dev.connect() == True, "Expected a True returned from Mock object."
    assert bt_dev._sock, "Sock (Bluetooth socket) should be set if connection is made."

def test_sending_to_disconnected_device():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    message_name = "Sanity_Adjust_Servo_180"

    ble_dev = Bt_Ble_Device(addr, name)
    ble_dev.is_connected = MagicMock(return_value=False)
    assert ble_dev.send_message(message_name) == False, "Expected False to be returned since device is disconnected"

    bt_dev = Bt_Device(addr, name)
    bt_dev.is_connected = MagicMock(return_value=False)
    assert bt_dev.send_message(message_name) == False, "Expected False to be returned since device is disconnected"

def test_sending_wrong_message_name():
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    wrong_message_name = "Sanity_Adjust_Servo_1000000"

    ble_dev = Bt_Ble_Device(addr, name)
    ble_dev.is_connected = MagicMock(return_value=True)     # Mocking device to be connected state
    print("\nExpecting an NameError Exception to be raised here and handled.")
    assert ble_dev.send_message(wrong_message_name) == False, "Expected an exception to be handled and False to be returned."

    bt_dev = Bt_Device(addr, name)
    bt_dev.is_connected = MagicMock(return_value=True)      # Mocking device to be connected state
    print("\nExpecting an NameError Exception to be raised here and handled.")
    assert bt_dev.send_message(wrong_message_name) == False, "Expected an exception to be handled and False to be returned."

def test_setting_wrong_message_fields(monkeypatch):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    correct_message_name = "Sanity_Adjust_Servo_180"

    def _mock_read(self):
        print(f"Mocking '_read' function in {type(self).__name__} to return a dummy Response packet data (8-bytes of 0s).")
        return bytes(8)

    def _mock_write(self, msg):
        print(f"Mocking '_write' function in {type(self).__name__} to check for attribute 'error_field'.")
        assert hasattr(msg.structure, "error_field") == False, "Expected the non-existent field name not to be present"
        print("Element 'error_field' not found!")

    monkeypatch.setattr(Bt_Ble_Device, "_write", _mock_write)       # Mocking '_write' to check for field name.
    monkeypatch.setattr(Bt_Device, "_write", _mock_write)

    monkeypatch.setattr(Bt_Ble_Device, "_read", _mock_read)         # Mocking '_read' to return 8-bytes of 0s regardless
    monkeypatch.setattr(Bt_Device, "_read", _mock_read)

    ble_dev = Bt_Ble_Device(addr, name)
    ble_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    assert ble_dev.send_message(correct_message_name, error_field=10)

    bt_dev = Bt_Device(addr, name)
    bt_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    assert bt_dev.send_message(correct_message_name, error_field=10)

def test_overwritting_existing_message_field(monkeypatch):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    correct_message_name = "Sanity_Adjust_Servo_180"
    expected_command_field_value = 0xFF

    def _mock_read(self):
        print(f"Mocking '_read' function in {type(self).__name__} to return a dummy Response packet data (8-bytes of 0s).")
        return bytes(8)

    def _mock_write(self, msg):
        print(f"Mocking '_write' function in {type(self).__name__} to confirm value of 'command' is overwritten.")
        assert hasattr(msg.structure, "command") == True, "Expected the presence of field 'command'."
        assert msg.structure.command == expected_command_field_value, "Expected the value of 'command' to be overwritten to 0xFF."
        print("Element 'command' successfully overwritten!")

    monkeypatch.setattr(Bt_Ble_Device, "_write", _mock_write)  # Mocking '_write' to check for field name and value.
    monkeypatch.setattr(Bt_Device, "_write", _mock_write)

    monkeypatch.setattr(Bt_Ble_Device, "_read", _mock_read)  # Mocking '_read' to return 8-bytes of 0s regardless
    monkeypatch.setattr(Bt_Device, "_read", _mock_read)

    ble_dev = Bt_Ble_Device(addr, name)
    ble_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    assert ble_dev.send_message(correct_message_name, command=expected_command_field_value)

    bt_dev = Bt_Device(addr, name)
    bt_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    assert bt_dev.send_message(correct_message_name, command=expected_command_field_value)

def test_read_timeout_values():
    pass
    # TODO: Add some mock apis and test timeouts

def test_varying_return_bytes_from_read(monkeypatch):
    addr = "FF:FF:FF:FF:FF:FF"
    name = "test"
    correct_message_name = "Sanity_Adjust_Servo_180"
    resp_msg_union = Response_Message_Union()
    resp_msg_union.structure.status = 0xFF
    mock_method = Mock()
    mock_method.side_effect = [None, None, bytes(7), bytes(7), resp_msg_union.bytes, resp_msg_union.bytes, bytes(8), bytes(8)]

    monkeypatch.setattr(Bt_Ble_Device, "_write", lambda self, msg: True)  # Mocking '_write' to return True.
    monkeypatch.setattr(Bt_Device, "_write", lambda self, msg: True)

    ble_dev = Bt_Ble_Device(addr, name)
    ble_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    ble_dev._read = mock_method
    bt_dev = Bt_Device(addr, name)
    bt_dev.is_connected = MagicMock(return_value=True)  # Mocking device to be connected state
    bt_dev._read = mock_method

    print(f"Mocking '_read' function to return None. Expecting False to be returned")
    assert ble_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving an incomplete packet size."
    assert bt_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving an incomplete packet size."

    print(f"Mocking '_read' function to return 7 bytes (Incomplete). Expecting False to be returned")
    assert ble_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving an incomplete packet size."
    assert bt_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving an incomplete packet size."

    print(f"Mocking '_read' function to return a complete return packet with a failed status; i.e. status != 0. Expecting False to be returned")
    assert ble_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving a non-zero status."
    assert bt_dev.send_message(correct_message_name) == False, "Expected a False returned after receiving a non-zero status."

    print("Mocking '_read' function to return a complete return packet with a passing status; i.e. status == 0. Expecting True to be returned")
    assert ble_dev.send_message(correct_message_name) == True, "Expected a True returned for this happy-path."
    assert bt_dev.send_message(correct_message_name) == True, "Expected a True returned for this happy-path."