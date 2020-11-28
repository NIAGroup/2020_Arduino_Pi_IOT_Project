"""
File:
    test_messages.py
Description:
    Unit test file for testing message structures and unions for size and format conformity.
Author:
    Adoany Berhe
"""
import __init__
from ctypes import *
import pdb

def test_base_message_struct(message_classes):
    for msg_obj in message_classes:
        if msg_obj.__name__ == "Message_Struct":
            assert sizeof(msg_obj) == 0, "Base class size is higher than 0. Unexpected fields introduced."
            assert '__str__' in msg_obj.__dict__, "Base class __str__ function removed!"
            assert msg_obj._pack_ == 1, "Base class is expected to be pack 1."
            assert msg_obj._fields_ == [], "Either _fields_ not defined or unexpected elements added in base class."
            return

    assert False, "Message_Struct class was not found. Must have been deleted!"

def test_base_message_union(message_classes):
    for msg_obj in message_classes:
        if msg_obj.__name__ == "Message_Union":
            assert sizeof(msg_obj) == 0, "Base class size is higher than 0. Unexpected fields introduced."
            assert '__str__' in msg_obj.__dict__, "Base class __str__ function removed!"
            assert '__init__' in msg_obj.__dict__, "Base Union class __init__ function removed!"
            assert msg_obj._pack_ == 1, "Base class is expected to be pack 1."
            assert msg_obj._fields_ == [], "Either _fields_ not defined or unexpected elements added in base class."
            return

    assert False, "Message_Union class was not found. Must have been deleted!"

def test_base_request_message_struct(message_classes):
    for msg_obj in message_classes:
        if msg_obj.__name__ == "Request_Message":
            assert sizeof(msg_obj) == 1, "Request Message Structure is expected to be 1 byte in size."
            assert msg_obj.command, "command field was removed or misspelled from Request Message Structure."
            return
    assert False, "Request_Message class was not found. Must have been deleted!"

def test_derived_message_structs(message_classes):
    base_class_structs = ["Message_Struct", "Request_Message"]
    for msg_obj in message_classes:
        if not (msg_obj.__name__ in base_class_structs) and not ("Union" in msg_obj.__name__):
            assert sizeof(msg_obj) == 8, f"{msg_obj.__name__} size is expected to be 8 bytes."
            assert msg_obj.command, f"command field missing from {msg_obj.__name__} class."
            if msg_obj.__name__ == "Response_Message":
                assert msg_obj.status, "status field missing from Response_Message class."
            elif msg_obj.__name__ == "PID_Controller_Message":
                assert msg_obj.angle, "angle field missing from PID_Controller_Message class."
                assert msg_obj.algorithm, "algorithm field missing from PID_Controller_Message class."
                assert msg_obj.kp, "kp field missing from PID_Controller_Message class."
                assert msg_obj.ki, "ki field missing from PID_Controller_Message class."
                assert msg_obj.kd, "angle field missing from PID_Controller_Message class."

def test_derived_message_unions(message_classes, message_structure_names):
    # Remove base classes
    message_structure_names.remove("Message_Struct")
    message_structure_names.remove("Request_Message")

    for msg_obj in message_classes:

        if ("Union" in msg_obj.__name__) and (msg_obj.__name__ != "Message_Union"):
            assert msg_obj.structure, f"structure field missing from {msg_obj.__name__}."
            assert msg_obj.bytes, f"bytes field missing from {msg_obj.__name__}."
            assert type(msg_obj().structure).__name__ in message_structure_names, f"{msg_obj.__name__}'s structure element " \
                                        f"({type(msg_obj().structure).__name__})does not match other message classes."

            message_structure_names.remove(type(msg_obj().structure).__name__)

    assert len(message_structure_names) == 0, ",".join(y for y in message_structure_names) + " message classes don't have Unions"