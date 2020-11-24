import __init__
from ctypes import Structure, Union, c_uint8, sizeof, resize


# -------------- Base Message Structures ---------------------#


class Message_Struct(Structure):
    """

    """
    _pack_ = 1
    _fields_ = []

    def __str__(self):
        """

        """
        field_name_idx = 0
        retStr = ""
        retStr += f"{type(self).__name__} \n".rjust(20)
        for field_tuple in super(type(self), self)._fields_:
            if "reserved" in field_tuple[field_name_idx]:
               continue
            else:
                _val = getattr(self,field_tuple[field_name_idx])
                retStr += f"{field_tuple[field_name_idx]}\t\t{_val} ({hex(_val)})\n"

        for field_tuple in self._fields_:
            if "reserved" in field_tuple[field_name_idx]:
                continue    # skip all reserved fields from parsing
            else:
                _val = getattr(self, field_tuple[field_name_idx])
                retStr += f"{field_tuple[field_name_idx]}\t\t{_val} ({hex(_val)})\n"

        return retStr

class Message_Union(Union):
    """

    """
    _pack_ = 1
    _fields_ = []

    def __init__(self):
        pass

    def __str__(self):
        """

        """
        try:
            return str(self.structure)
        except AttributeError:
            print(f"'Structure' field not implemented in message payload union.\n")

class Response_Message(Message_Struct):
    """

    """
    _fields_ = [
        ("status",          c_uint8),
        ("command",         c_uint8),
        ("byte_0",          c_uint8, 1),
        ("byte_1",          c_uint8, 1),
        ("byte_2",          c_uint8, 1),
        ("byte_3",          c_uint8, 1),
        ("byte_4",          c_uint8, 1),
        ("byte_5",          c_uint8, 1),
        ("reserved",        c_uint8, 2),    # One Status byte + Reserved byte = 2 Reserved
        ("reservedBytes",   c_uint8 * 5)
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
    _fields_ = [
        ("command",         c_uint8),
    ]


#------------------ Derived Message Structures -----------------#


class Sanity_BT_Echo_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_BT_Echo_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_BT_Echo_Message),
        ("bytes",           sizeof(Sanity_BT_Echo_Message) * c_uint8)
    ]
    def __init__(self):
        """

        """
        self.structure.command = 0x80

class Sanity_Adjust_Servo_180_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_180_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_180_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_180_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x9B

class Sanity_Adjust_Servo_150_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_150_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_150_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_150_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x98

class Sanity_Adjust_Servo_120_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_120_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_120_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_120_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x94

class Sanity_Adjust_Servo_90_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_90_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_90_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_90_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x90

class Sanity_Adjust_Servo_60_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_60_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_60_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_60_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x92

class Sanity_Adjust_Servo_30_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_30_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_30_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_30_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x91

class Sanity_Adjust_Servo_0_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Adjust_Servo_0_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Adjust_Servo_0_Message),
        ("bytes",           sizeof(Sanity_Adjust_Servo_0_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x93

class Sanity_Loop_Servo_180_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Loop_Servo_180_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Loop_Servo_180_Message),
        ("bytes",           sizeof(Sanity_Loop_Servo_180_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0x96

class Sanity_Blink_Yellow_LED_Message(Request_Message):
    """

    """
    _fields_ = [
        ("reservedBytes",   c_uint8 * 7)
    ]

class Sanity_Blink_Yellow_LED_Message_Union(Message_Union):
    """

    """
    _fields_ = [
        ("structure",       Sanity_Blink_Yellow_LED_Message),
        ("bytes",           sizeof(Sanity_Blink_Yellow_LED_Message) * c_uint8)
    ]

    def __init__(self):
        """

        """
        self.structure.command = 0xA0

class PID_Controller_Message(Request_Message):
    """

    """
    _fields_ = [
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

    def __init__(self):
        """

        """
        self.command = 0x70
