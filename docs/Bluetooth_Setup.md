## Python Bluetooth Setup - _python 3.7_

1. Install pybluez   
`sudo python 3.7 -m pip install pybluez`
> NOTE : This will only allow simple python programming for bluetooth classic, but not BLE (bluetooth Low Energy Devices)
2. Run the following install command:  
`sudo apt-get install libbluetooth-dev`   
> NOTE : As of the current date _(July 30, 2020)_ there is an issue with the BLE portion of the pybluez library, so this must be installed before the necessary additional python libraries can be installed. 
3. Install gattlib:
```
sudo python3.7 -m pip install gattlib
```

4. Normally accessing the Bluetooth stack is reserved for root; to allow non-root access to the Bluetooth stack we can give Python 3 and hcitool the missing capabilities to access the Bluetooth stack.:
```
sudo apt-get install libcap2-bin
sudo setcap 'cap_net_raw,cap_net_admin+eip' `readlink -f \`which python3\``
sudo setcap 'cap_net_raw+ep' `readlink -f \`which hcitool\`
```


5. You should now be able to run the following script as a test:
```
# simple inquiry example - non-bluetooth LE enabled devices only
import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print("  {} - {}".format(addr, name))
    
# bluetooth low energy scan
from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
```
