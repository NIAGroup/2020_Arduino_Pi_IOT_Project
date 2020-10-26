import __init__
from ctypes import Structure, Union, c_uint8, sizeof

class Message_Struct(Structure):
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

class Message_Union(Union):
    """
    
    """
    _pack_ = 1
    _fields_ = []

class Response_Message(Message_Struct):
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

class Response_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Response_Message),
        ("bytes",           sizeof(Response_Message) * c_uint8)
    ]


class Request_Message(Message_Struct):
    """

    """
    _pack_ = 1
    _fields_ = [
        ("command",         c_uint8),
    ]

class Request_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Request_Message),
        ("bytes",           sizeof(Request_Message) * c_uint8)
    ]


class Sanity_Bt_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_Bt_Message_Union(Message_Union):
    """

    """
    pass


class Sanity_Servo_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_Servo_Message_Union(Message_Union):
    """

    """
    pass


class Sanity_Sensor_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_Sensor_Message_Union(Message_Union):
    """

    """
    pass


class Sanity_PID_Message(Request_Message):
    """

    """
    _fields_ = Request_Message._fields_

class Sanity_PID_Message_Union(Message_Union):
    """

    """
    pass


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

class PID_Controller_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       PID_Controller_Message),
        ("bytes",           sizeof(PID_Controller_Message) * c_uint8)
    ]