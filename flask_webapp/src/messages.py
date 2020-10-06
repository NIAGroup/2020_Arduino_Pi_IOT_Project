from ctypes import *
from copy import deepcopy

class Message(Structure):
    """

    """
    _pack_ = 1
    _fields_ = []

    def __str__(self):
        """

        """
        name_pos = 0
        retStr = ""
        retStr += f"{type(self).__name__} \n".rjust(20)
        for field in self._fields_:
            if field[name_pos] == "reserved":
                continue    # skip all reserved fields from parsing
            retStr += f"{field[name_pos]}\t\t\t{getattr(self, field[name_pos])} \n"

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

class Response_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          Response_Message),
        ("bytes",           sizeof(Response_Message) * c_uint8),
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
    _fields_ = deepcopy(Request_Message._fields_)

class Sanity_Bt_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          Sanity_Bt_Message),
        ("bytes",           sizeof(Sanity_Bt_Message) * c_uint8),
    ]

class Sanity_Servo_Message(Request_Message):
    """

    """
    _fields_ = deepcopy(Request_Message._fields_)

class Sanity_Servo_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          Sanity_Servo_Message),
        ("bytes",           sizeof(Sanity_Servo_Message) * c_uint8),
    ]

class Sanity_Sensor_Message(Request_Message):
    """

    """
    _fields_ = deepcopy(Request_Message._fields_)

class Sanity_Sensor_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          Sanity_Sensor_Message),
        ("bytes",           sizeof(Sanity_Sensor_Message) * c_uint8),
    ]

class Sanity_PID_Message(Request_Message):
    """

    """
    _fields_ = deepcopy(Request_Message._fields_)

class Sanity_PID_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          Sanity_PID_Message),
        ("bytes",           sizeof(Sanity_PID_Message) * c_uint8),
    ]

class PID_Controller_Message(Request_Message):
    """

    """
    _fields_ = deepcopy(Request_Message._fields_)
    _fields_ += [
        ("angle",           c_uint8),
        ("algorithm",       c_uint8),
        ("kp",              c_uint8),
        ("ki",              c_uint8),
        ("kd",              c_uint8),
        ("reserved",        c_uint8 * 2)
    ]

class PID_Controller_Message_Union(Union):
    """

    """
    _fields_ = [
        ("struct",          PID_Controller_Message),
        ("bytes",           sizeof(PID_Controller_Message) * c_uint8),
    ]

