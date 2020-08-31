import bluetooth
from bluetooth.ble import DiscoveryService

class BtDevContainer(object):
    """
    :brief BtDevContainer: Container class for holding all bt device instances and apis
    :description: This class will discover all peripheral devices and provide APIs for sending and receiving
        commands.
    :methods: issue dict(BtDevContainer)
    """
    def __init__(self):
        """

        """
        self._bt_devices_ = {}  # addr -> name
        self.scan_for_bt_ble_devices()
        self.scan_for_bt_regular_devices()
        if self.verify_scanned_device():
            print(f"Discovered {len(self._bt_devices_.keys())} valid bluetooth devics.")


    def scan_for_bt_regular_devices(self):
        """
        :brief scan_for_bt_regular_devices: scan for regular bluetooth devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        devices = bluetooth.discover_devices(lookup_names=True)
        for name, addr in devices:
            self._bt_devices_[addr] = name


    def scan_for_bt_ble_devices(self):
        """
        :brief scan_for_bt_ble_devices:  scan for ble devices and collect into a list.
        :description: The following function will be used to scan for bt devices within a 30m radius of
            the raspberry pi.
        """
        service = DiscoveryService()
        devices = service.discover(2)
        for addr, name in devices:
            self._bt_devices_[addr] = name

    def verify_scanned_device(self):
        """
        :brief verify_scanned_device: iterate through scanned lists and verify it's device under test.
        :description: This function will be used for issuing a test to identify desired arduino devices
            in the bluetooth range.
        :return: True if at least a single device is configured for test, False if none were found.
        """
        retVal = False
        if self._bt_devices_:
            for addr in self._bt_devices_.keys():
                # TODO figure out what message will identify the arduino DUT
                print(addr)
            retVal = True
        else:
            print("No bluetooth devices discovered. _bt_devices_ dictionary empty.")

        return retVal

    def send_bluetooth_msg(self, addr, msg):
        """
        :brief send_bluetooth_msg(addr, msg): generic message sending api.
        :description: This function will be used to issue any commands to the peripheral device and return
            values if any.
        :param addr: bluetooth address of peripheral device.
        :param msg: bluetooth message to be sent to the peripheral device.
        :return:
        """
        # Todo: come up with a generic API