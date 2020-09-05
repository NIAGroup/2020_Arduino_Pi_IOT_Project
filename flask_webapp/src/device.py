from messages import *

class Bt_Ble_Device(object):
    """

    """
    def __init__(self, addr):
        """
        :brief __init__(addr): Initializer to Bt_Ble_Device.
        :param addr: address of the device.
        """
        self._addr = addr
        self._dev = btle.Peripheral(addr)
        self._services = list(self._dev._services)
        self._characteristic = self._services[len(self._services) - 1].getCharacteristics()[0]

    def __del__(self):
        """

        """
        self._dev.disconnect()
        del self._dev

    def _write(self, msg):
        """

        """
        self._characteristic.write(msg)

    def _read(self):
        """

        """
        pass    # Todo: Define read interface and parse response packet

    def send_message(self, msgName):
        """
        """
        msg_type = eval(f"{msgName}_Message")
        msg_obj = msg_type()    # Todo: Probably need a try-except here
        msg_bytes = msg_obj.bytes()  # Todo: Figure this out
        self._write(msg_bytes)
        self._read()
        return True

class Bt_Device(object):
    """

    """
    pass