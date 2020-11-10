"""
File:
    device_delegate.py
Description:
    Describes bluetooth delegates for getting notifications when read bytes are ready.
Classes:
    BtleDelegate
Author(s):
    Princton Brennan, Adonay Berhe
"""
import __init__
from bluepy import btle

class BtleDelegate(btle.DefaultDelegate):
    """

    """
    def __init__(self, handle):
        """
        Brief:
            __init__(): Initializer to BtleDelegate.
        Param(s):
            char: Integer handle for the characteristic of the desired peripheral
        """
        btle.DefaultDelegate.__init__(self)
        self._char_handle = handle
        self.response_message_data = None
        self.response_message_handle = None

    def handleNotification(self, cHandle, data):
        """
        Brief:
            handleNotification(cHandle, data) - callback api called upon received signaled.
        Param(s):
            cHandle: is the (integer) handle for the characteristic data is sent from.
                This distinguishes between notifications from multiple sources on the same peripheral
            data: The characteristic data (a str type on Python 2.x, and bytes on 3.x)
        Return:
            bytes being read.
        """
        self.response_message_handle = cHandle
        #if self.response_message_handle == self._char_handle:
        self.response_message_data = data
