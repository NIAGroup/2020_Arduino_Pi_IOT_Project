# The import below is referencing the pybluez library
import bluetooth
from bluetooth.ble import DiscoveryService
import json 

"""
The following function will be used to scan for bt
devices within a 30m radius of the raspberry pi
"""
def scanForBTDevices():
  """
  A dictionary is created to store the list of scanned bt
  devices defining the difference between classic bluetooth
  devices and ble or ble compatiable devices.
  """
  bt_devices = {
          "devices_classic" : {0: {}},
          "devices_ble" : {0:{}}
  }

  devices = bluetooth.discover_devices(duration=10,lookup_names=True)
  i = 0
  for dev in devices:
      x,y = dev
      bt_devices["devices_classic"][i] = {"name": y, "addr": x} 
      i+=1

  service = DiscoveryService()
  devices = service.discover(2)
  i=0
  for key in devices.keys():
      bt_devices["devices_ble"][i] = {"name" : devices[key],"addr": key}
      i+=1
  """
  The next line converts the dictionary to a json object that will be 
  easily readable for the backend developer to read and have the front-end
  developer to display on the UI.
  """
  json_devices = json.dumps(bt_devices, indent=4)
  print(json_devices)

scanForBTDevices()
