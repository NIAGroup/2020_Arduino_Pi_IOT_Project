from device_list import *
x = BtDevContainer()
x.scan()
x.get_device('Arduino_PID_0').connect()
x.get_device('Arduino_PID_0').send_message('Sanity_Bt')

import pdb; pdb.set_trace()
