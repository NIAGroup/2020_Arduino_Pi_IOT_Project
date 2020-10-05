import bluetooth, subprocess, time

def RequestConfirmation(self, device, passkey):
        #### my code
        set_trusted(device)
        return
        #### my code
        print("RequestConfirmation (%s, %06d)" % (device, passkey))
        confirm = ask("Confirm passkey (yes/no): ")
        if (confirm == "yes"):
            set_trusted(device)
            return
        raise Rejected("Passkey doesn't match")

def RequestAuthorization(self, device):
        #### my code
        return
        #### my code
        print("RequestAuthorization (%s)" % (device))
        auth = ask("Authorize? (yes/no): ")
        if (auth == "yes"):
            return
        raise Rejected("Pairing rejected")
    
addr = "00:14:03:06:12:84"

name = "ArduinoBtOG_0"      # Device name
addr = addr      # Device Address
port = 1         # RFCOMM port
passkey = "1234" # passkey of the device you want to connect

