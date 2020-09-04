import bluetooth
from bluetooth.ble import DiscoveryService
from bluepy import *

class BtDevContainer(object):
    """
    :brief BtDevContainer(): Container class for holding all bt device instances and apis
    :description: This class will discover all peripheral devices and provide APIs for sending and receiving
        commands.
    :methods: issue dict(BtDevContainer)
    """
    def __init__(self):
        """

        """
        self._bt_name_addr = {}     # name -> addr
        self._bt_addr_dev = {}      # addr -> device

    def _scan_for_bt_regular_devices(self):
        """
        :brief _scan_for_bt_regular_devices(): scan for regular bluetooth devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        devices = bluetooth.discover_devices(lookup_names=True)
        for name, addr in zip(devices.keys(), devices.values()):
            self._bt_name_addr[name] = addr

    def _scan_for_bt_ble_devices(self):
        """
        :brief _scan_for_bt_ble_devices():  scan for ble devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        service = DiscoveryService()
        devices = service.discover(2)
        for addr, name in zip(devices.keys(), devices.values()):
            self._bt_name_addr[name] = addr
            self._bt_addr_dev[addr] = self._get_ble_device(addr)

    def _get_ble_device(self, addr):
        """
        :brief _get_ble_device(addr): use the device address string to return a bluetooth device object.
        :description: Using the bluepy library we create a "Peripheral" object.
            NOTE : BLE connections work as a server-to-client (1-many) connection.
        :param addr: address string of the device in question.
        :return: a device handle of the client device or None.
        """
        dev = btle.Peripheral(addr)
        return dev

    def scan(self):
        """
        :brief scan(): public api for issuing a bluetooth device scan.
        :description: This api issues a scan for smart bluetooth and ble bluetooth devices; performs
            a verification test for filtering non-arduino devices and returns device names.
        :return: list of device name strings.
        """
        self._scan_for_bt_ble_devices()
        self._scan_for_bt_regular_devices()
        self.verify_scanned_device()
        active_dev_list = self._bt_name_addr.keys()
        print(f"Discovered {len(active_dev_list)} valid bluetooth devics.")
        return active_dev_list

    def verify_scanned_device(self):
        """
        :brief verify_scanned_device: iterate through scanned lists and verify it's device under test.
        :description: This function will be used for issuing a test to identify desired arduino devices
            in the bluetooth range.
        """
        if self._bt_name_addr:
            for name in self._bt_name_addr.keys():
                if name != "arduino": # Todo: Find out device name
                    self._bt_name_addr.pop(name)
        else:
            print("No bluetooth devices discovered. _bt_devices_ dictionary empty.")

    def send_bluetooth_msg(self, name, msg):
        """
        :brief send_bluetooth_msg(addr, msg): generic message sending api.
        :description: This function will be used to issue any commands to the peripheral device and return
            values if any.
        :param name: bluetooth device name.
        :param msg: bluetooth message to be sent to the peripheral device.
        :return: True on success, False on failure.
        """
        # Todo: come up with a generic API

class Bt_Device(object):
    """

    """
    def __init__(self, name, addr, is_ble=True):
        """
        :brief __init__(name, addr, dev, is_ble=True): Initializer to Bt_Device.
        :param name: name of the device.
        :param addr: address of the device.
        :param is_ble: Flag to differentiate between regular and ble bluetooth device.
        """
        _name = name
        _addr = addr
        _is_ble = is_ble
        _characteristic = None
        if _is_ble:
            _dev = btle.Peripheral(addr)
            services = list(_dev.services)
            _characteristic = services[len(services) - 1].getCharacteristics()[0]

    def __del__(self):
        """

        """
        self._dev.disconnect()
        del self._dev

    def _send(self, msg):
        """

        """
        self._characteristic.write(msg)

    def send_command(self, msgName):
        """
        """
