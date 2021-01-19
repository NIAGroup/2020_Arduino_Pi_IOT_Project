"""
File:
    device_list.py
Description:
    Describes bluetooth device container for managing device instances.
Classes:
    Bt_Dev_Container
Author:
    Adoany Berhe
"""
import __init__
import bluetooth
from bluetooth.ble import DiscoveryService
from device import Bt_Ble_Device, Bt_Device

RETURN_STATUS = {
        "SUCCESS": 0x00,
        "ALREADY_CONNECTED": 0x01,
        "CONNECTION_FAILED": 0x02,
        "ERROR": 0xFF
    }

class Bt_Dev_Container(object):
    """
    Brief:
        Bt_Dev_Container(): Container class for holding all bt device instances and apis
    Description:
        This class will discover all peripheral devices and provide APIs for sending and receiving
            commands.
    Methods:
        _scan_for_bt_regular_devices, _scan_for_bt_ble_devices, _is_verified_bt_dev, get_device
    """
    def __init__(self):
        """
        Brief:
            __init__(): Initializer to bluetooth device container object.
        Param(s):

        """
        self._bt_name_dev_dict = {}     # name -> device
        self._connected_dev = None
    @property
    def connected_device(self):
        """

        """
        return self._connected_dev

    def _scan_for_bt_regular_devices(self):
        """
        Brief:
            _scan_for_bt_regular_devices(): scan for regular bluetooth devices and collect into a list.
        Description:
            The following function will be used to scan for bt devices within a 30m radius of
                the raspberry pi.
        """
        devices = bluetooth.discover_devices(lookup_names=True)
        for addr, name in devices:
            if self._is_verified_bt_dev(name):
                self._bt_name_dev_dict[name] = Bt_Device(addr, name)

    def _scan_for_bt_ble_devices(self):
        """
        Brief:
            _scan_for_bt_ble_devices():  scan for ble devices and collect into a list.
        Description:
            The following function will be used to scan for bt devices within a 30m radius of
                the raspberry pi.
        """
        service = DiscoveryService()
        devices = service.discover(2)
        for addr, name in zip(devices.keys(), devices.values()):
            if self._is_verified_bt_dev(name):
                self._bt_name_dev_dict[name] = Bt_Ble_Device(addr, name)

    def _is_verified_bt_dev(self, name):
        """
        Brief:
            _is_verified_bt_dev(name): verify the dev object is desired device under test.
        Description:
            This function will be used for issuing a test to identify desired arduino devices
                in the bluetooth range.
        Param(s):
            name: name of the device that appeared in a bluetooth scan.
        Return:
            True on verified device, False on every other component.
        """
        return "arduino" in name.lower()

    def scan(self):
        """
        Brief:
            scan(): public api for issuing a bluetooth device scan.
        Description:
            This api issues a scan for smart bluetooth and ble bluetooth devices; performs
                a verification test for filtering non-arduino devices and returns device names.
        Return:
            list of device name strings.
        """
        self._scan_for_bt_ble_devices()
        self._scan_for_bt_regular_devices()
        active_dev_list = list(self._bt_name_dev_dict.keys())
        print(f"Discovered {len(active_dev_list)} valid bluetooth devics.")
        return active_dev_list

    def get_device(self, name):
        """
        Brief:
            get_device(name): returns a bluetooth device objects.
        Description:
            This function takes a name string of the desired device, checks if object instance
                exists (checks for key-value exceptions) and returns either object or None with message.
        Param(s):
            name: string value of the device name.
        Return
            Bt_Device or Bt_Ble_Device device instance on success; Raise an exception upon error/failure.
        """
        try:
            return self._bt_name_dev_dict[name]
        except KeyError:
            print(f"Device name: {name} is not found. Raising exception.\n{KeyError}")
            raise KeyError
        except Exception:
            print(f"An unexpected exception occurred down the stack. Re-raising exception.")
            raise Exception

    def connect_device(self, name):
        """

        """
        if self.get_device(name).is_connected():
            print("Device is already connected.")
            self._connected_dev = name
            return RETURN_STATUS["ALREADY_CONNECTED"]
        else:
            try:
                if self._connected_dev:     # disconnect the previously connected device
                    self.disconnect_device(self._connected_dev)

                # connect the new device
                if self.get_device(name).connect():
                    self._connected_dev = name
                    return RETURN_STATUS["SUCCESS"]
                else:
                    print(f"Connect command failed for device {name}")
                    return RETURN_STATUS["CONNECTION_FAILED"]
            except Exception as error:
                print(f"An unexpected error happened. \n{error}")
                raise error

    def disconnect_device(self, name):
        """

        """
        self.get_device(name).disconnect()
        self._connected_dev = None      # reset connected_device to None

