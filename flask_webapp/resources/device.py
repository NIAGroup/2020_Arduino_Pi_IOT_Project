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
            #devices = Container.scan()
            #retDict["scan_devs"] = devices
            retDict["scan_devs"] = ['test1', 'test2', 'test3', 'test4']

            # update database
            for deviceName in retDict["scan_devs"]:
                print(f'scanned dev: {deviceName}')
                if ScanDeviceModel.find_by_name(deviceName):
                    print(f'scan device already exist: {deviceName}')
                else:
                    print(f"found a new new device: {deviceName}")
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
        retValue = {}
        for deviceName in devices["selectedDevices"]:
            print(f'debug: {deviceName}')
            """
            try:
                retValue[deviceName] = Container.get_device(deviceName).connect()
            except Exception:
                retValue[deviceName] = False
            """
            device = DeviceModel.find_by_name(deviceName)
            if device:
                print(f"connecting existing device {deviceName}")
                device.status = "connected"
            else:
                print(f"Adding a new device: {deviceName}")
                device = DeviceModel(deviceName, "connected")
            device.save_to_db()

        return device.json(), 201

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
        retValue = {}
        for deviceName in devices["selectedDevices"]:
            # try block is failing calling Container.remove_device()
            # try:
            #     Container.remove_device(deviceName)
            #     retValue[device] = True
            #     # update database
            #     device = DeviceModel.find_by_name(deviceName)
            #     if device:
            #         print("Disconnecting device")
            #         device.status = "disconnected"
            #         #device = DeviceModel(name, data['status'])
            #     else:
            #         #device.status = data['status'] # update the status
            #         #device = DeviceModel(name, data['status'])
            #         print("Adding a new device")
            #         device = DeviceModel(deviceName, "connected")
            #
            #     device.save_to_db()
            # except Exception:
            #     print("In exception")
            #     retValue[deviceName] = False

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
