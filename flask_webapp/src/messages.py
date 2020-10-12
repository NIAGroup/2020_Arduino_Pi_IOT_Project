import __init__
from ctypes import *

class Message(Structure):
    """

    """
    _pack_ = 1
    _fields_ = []

    def __str__(self):
        """

        """
        retStr = ""
        retStr += f"{type(self).__name__} \n".rjust(20)
        for field_name, field_type in self._fields_:
            if field_name == "reserved":
                continue    # skip all reserved fields from parsing
            retStr += f"{field_name}                {getattr(self, field_name)} \n"

        return retStr

class Response_Message(Message):
    """

    """
    _pack_ = 1
    _fields_ = [
        ("status",          c_uint8),
        ("byte_0",          c_uint8, 1),
        ("byte_1",          c_uint8, 1),
        ("byte_2",          c_uint8, 1),
        ("byte_3",          c_uint8, 1),
        ("byte_4",          c_uint8, 1),
        ("byte_5",          c_uint8, 1),
        ("reserved",        c_uint8, 2),
    ]

class Request_Message(Message):
    """

    """
    _pack_ = 1
    _fields_ = [
        ("command",         c_uint8),
    ]

class Sanity_Bt_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_Servo_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_Sensor_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_PID_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class PID_Controller_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_
    _fields_ += [
        ("angle",           c_uint8),
        ("algorithm",       c_uint8),
        ("kp",              c_uint8),
        ("ki",              c_uint8),
        ("kd",              c_uint8),
        ("reserved",        c_uint8 * 2)
    ]