from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.device import DeviceModel
from models.scan_device import ScanDeviceModel

class BluetoothDevice(Resource):
    def get(self):
        """
        Brief:
        Param(s):
        Return:
        """
        retDict = {}
        try:
            # devices = Container.scan()
            # retDict["scan_devs"] = devices
            # test on Windows
            retDict["scan_devs"] = ['test1', 'test2', 'test3', 'test4']
            # update database
            for deviceName in retDict["scan_devs"]:
                print(f'scanned device: {deviceName}')
                if ScanDeviceModel.find_by_name(deviceName):
                    print(f'scan device already exist: {deviceName}')
                else:
                    device = ScanDeviceModel(deviceName)
                    device.save_to_db()
        except Exception as e:
            print(f"Runtime error has occurred. {e}")

        return jsonify(retDict)


class Connect(Resource):
    def get(self,name):
        device = DeviceModel.find_by_name(name)
        if device:
            return device.json()
        return {'message':'Device not found'}, 404

    def post(self):
        devices = request.get_json()
        print(f'devices => {devices}')
        retValue = {"connectedDevice": {}}

        for deviceName in devices["selectedDevices"]:
            print(f'debug: processing {deviceName}')
            # This try block is failing
            # try:
            #     retValue["connectedDevice"][deviceName] = Container.get_device(deviceName).connect()
            #     # update database
            #     device = DeviceModel.find_by_name(deviceName)
            #     if device:
            #         # Connecting existing device
            #         device.status = "connected"
            #     else:
            #         # Adding a new device
            #         device = DeviceModel(deviceName, "connected")
            #     device.save_to_db()
            # except Exception:
            #     print("debug: try failed")
            #     retValue["connectedDevice"][deviceName] = False
                # update database
            device = DeviceModel.find_by_name(deviceName)
            if device:
                # Connecting existing device
                device.status = "connected"
            else:
                # Adding a new device
                device = DeviceModel(deviceName, "connected")
            device.save_to_db()

        return jsonify(retValue)

    def delete(self,name):
        device = DeviceModel.find_by_name(name)
        if device:
            device.delete_from_db()

        return {'message', 'device deleted'}


class Disconnect(Resource):
    def post(self):
        """
        Brief:
        Param(s):
        Return:
        """
        devices = request.get_json()
        print(f'devices => {devices}')
        retValue = {"disconnectedDevice": {}}
        for deviceName in devices["selectedDevices"]:
            # try block is failing
            # try:
            #     Container.get_device(deviceName).disconnect()
            #     retValue["disconnectedDevice"][device] = True
            #     retValue[deviceName] = True
            #     # Update db to disconnected status
            #     device = DeviceModel.find_by_name(deviceName)
            #     if device:
            #         print(f"Disconnecting device {deviceName}")
            #         device.status = "disconnected"
            #     device.save_to_db()
            # except Exception as error:
            #     print(f"Unexpected error occurred. {error}")
            #     retValue["disconnectedDevice"][deviceName] = False
            # Update db to disconnected status
            device = DeviceModel.find_by_name(deviceName)
            if device:
                print(f"Disconnecting device {deviceName}")
                device.status = "disconnected"
            device.save_to_db()
        return jsonify(retValue)


class DeviceList(Resource):
    def get(self):

        #return {'devices': list(map(lambda x: x.json(), DeviceModel.query.all()))}
        return {'devices': [device.json() for device in DeviceModel.query.all()]}
