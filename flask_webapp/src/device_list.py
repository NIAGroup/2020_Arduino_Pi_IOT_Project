import bluetooth
from bluetooth.ble import DiscoveryService
from bluepy import *
from device import Bt_Ble_Device, Bt_Device

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
        self._bt_name_dev_dict = {}     # name -> device

    def _scan_for_bt_regular_devices(self):
        """
        :brief _scan_for_bt_regular_devices(): scan for regular bluetooth devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        devices = bluetooth.discover_devices(lookup_names=True)
        for device in devices:
            addr, name = device
            self._bt_name_dev_dict[name] = Bt_Device(addr)

    def _scan_for_bt_ble_devices(self):
        """
        :brief _scan_for_bt_ble_devices():  scan for ble devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        service = DiscoveryService()
        devices = service.discover(2)
        for addr, name in zip(devices.keys(), devices.values()):
            self._bt_name_dev_dict[name] = Bt_Ble_Device(addr)

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
        active_dev_list = self._bt_name_dev_dict.keys()
        print(f"Discovered {len(active_dev_list)} valid bluetooth devics.")
        return active_dev_list

    def verify_scanned_device(self):
        """
        :brief verify_scanned_device: iterate through scanned lists and verify it's device under test.
        :description: This function will be used for issuing a test to identify desired arduino devices
            in the bluetooth range.
        """
        if self._bt_name_dev_dict:
            for name in self._bt_name_dev_dict.keys():
                if "arduino" not in name.lower(): # Todo: Find out device name
                    self._bt_name_dev_dict.pop(name)
        else:
            print("No bluetooth devices discovered. _bt_devices_ dictionary empty.")

    def send_bluetooth_msg(self, name, msg_name):
        """
        :brief send_bluetooth_msg(addr, msg): generic message sending api.
        :description: This function will be used to issue any commands to the peripheral device and return
            values if any.
        :param name: bluetooth device name.
        :param msg_name: bluetooth message name string to be sent to the peripheral device.
        :return: True on success, False on failure.
        """
        retVal = False
        try:
            retVal = self._bt_name_dev_dict[name].send_message(msg_name)
        except ValueError as error:
            print(f"Device {name} does not exist.")
            retVal = False

        # Todo: Figure out a way to propagate error message
        return retVal



