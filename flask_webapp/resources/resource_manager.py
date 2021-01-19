from flask import request, jsonify, render_template, Response
from flask_restful import Resource
from flask_api import status
from models.device_db_model import Device_Model
from src.device_container import Bt_Dev_Container, RETURN_STATUS

Container = Bt_Dev_Container()

class Home_Manager(Resource):
    """

    """
    def get(self):
        return render_template("index.html"), status.HTTP_200_OK

class Scanlist_Manager(Resource):
    def get(self):
        """
        Brief:
        Param(s):
        Return:
        """
        retDict = {}
        resp_status = None
        try:
            devices = Container.scan()
            retDict["scanned_devices"] = devices      # Create the body/payload
            resp_status = status.HTTP_200_OK
        except Exception as e:
            error_str = f"Runtime error has occurred upon performing a scan.\n {e}"
            print(error_str)
            retDict["error_msg"] = error_str
            resp_status = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Connection_Manager(Resource):
    def get(self):
        retDict = {}
        resp_status = None
        devices = Device_Model.find_by_status("connected")

        if devices:
            if type(devices) is list:   # more than one connected device logged.
                error_str = f"Found multiple entries in the database with connected status. {devices}"
                print(error_str)
                resp_status = HTTP_512_DB_DOUBLE_ENTRY_ERROR = 512
                retDict["error_msg"] = error_str
            else:
                resp_status = status.HTTP_200_OK
                retDict["connected_device"] = devices.json()
        else:
            resp_status = status.HTTP_204_NO_CONTENT

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

    def post(self):
        devices = request.get_json()
        print(f'devices => {devices}')
        retDict = {}
        resp_status = None

        for deviceName in devices["selectedDevices"]:
            print(f'debug: processing {deviceName}')
            try:
                if deviceName != Container.connected_device():
                    ret_status = Container.connect_device(deviceName)

                    if ret_status == RETURN_STATUS["SUCCESS"]:     #if connect returned true

                        prev_connected_dev = Device_Model.find_by_status("connected")
                        if prev_connected_dev:  # check for previous connection
                            prev_connected_dev.status = "disconnected"
                            prev_connected_dev.save_to_db()
                            retDict["disconnected_device"] = prev_connected_dev.json()

                        device = Device_Model.find_by_name(deviceName)
                        if device:
                            # Connecting existing device
                            device.status = "connected"
                        else:
                            # Adding a new device
                            device = Device_Model(deviceName, "connected")
                        device.save_to_db()
                        retDict["connected_device"] = device.json()   # create the body/payload
                        resp_status = status.HTTP_201_CREATED

                    elif ret_status == RETURN_STATUS["ALREADY_CONNECTED"]:
                        resp_status = status.HTTP_202_ACCEPTED
                        # Confirm that db also reports the same thing
                        device = Device_Model.find_by_name(deviceName)
                        if (device == None) or (device.status != "connected"):
                            pass    # Todo: Figure out this edge condition
                        else:
                            retDict["connected_device"] = device.json()
                else:
                    resp_status = status.HTTP_202_ACCEPTED
                    # Confirm that db also reports the same thing
                    device = Device_Model.find_by_name(deviceName)
                    if (device == None) or (device.status != "connected"):
                        pass  # Todo: Figure out this edge condition
                    else:
                        retDict["connected_device"] = device.json()

            except Exception as error:
                error_str = f"An error occurred in the lower stack of the code. \n {error}"
                print(error_str)
                retDict["error_msg"] = error_str
                resp_status = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

    def delete(self,name):
        device = Device_Model.find_by_name(name)
        if device:
            device.delete_from_db()
        return {'message', 'device deleted'}

class Disconnection_Manager(Resource):
    def put(self):
        """
        Brief:
        Param(s):
        Return:
        """
        devices = request.get_json()
        print(f'devices => {devices}')
        retDict = {}
        resp_status = None
        for deviceName in devices["selectedDevices"]:
            try:
                Container.disconnect_device(deviceName)

                # Update db to disconnected status
                device = Device_Model.find_by_name(deviceName)
                if device:
                    print(f"Disconnecting device {deviceName}")
                    device.status = "disconnected"
                else:
                    print(f"Something weird is happening here. DB entry not found for device {deviceName}!!!")
                    device = Device_Model(deviceName, "disconnected")
                device.save_to_db()
                retDict["disconnected_device"] = device.json()
                resp_status = status.HTTP_202_ACCEPTED
            except Exception as error:
                error_str = f"Unexpected error occurred. {error}"
                print(error_str)
                retDict["error_msg"] = error_str
                resp_status = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Previous_Connection_Manager(Resource):
    def get(self):
        resp_status = status.HTTP_200_OK
        retDict = {'previously_paired_devices': [device.json() for device in Device_Model.query.all()]}
        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Functional_Test_Manager(Resource):
    def get(self):
        pass
    def post(self):
        pass

class PID_Command_Manager(Resource):
    def get(self):
        pass

    def post(self):
        """

        """
        pass

class Video_Feed_Manager(Resource):
    pass