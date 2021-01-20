from flask import request, jsonify, render_template, Response
from flask_restful import Resource
from flask_api import status
from models.device_db_model import Device_Model

class HOME(Resource):
    """

    """
    def get(self):
        return render_template("index.html"), status.HTTP_200_OK

class Previous_Connection_Resource(Resource):
    def get(self):
        resp_status = None
        retDict = {'previously_paired_devices': [device.json() for device in Device_Model.query.all()]}
        if len(retDict['previously_paired_devices']) == 0:      # Check if db has any devices logged.
            resp_status = status.HTTP_204_NO_CONTENT
        else:
            resp_status = status.HTTP_200_OK

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Scanlist_Resource(Resource):
    def get(self):
        """
        Brief:
        Param(s):
        Return:
        """
        retDict = {}
        retDict["scanned_devices"] = ['test1', 'test2', 'test3', 'test4']
        resp_status = status.HTTP_200_OK

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Device_Connection_Resource(Resource):
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
            print(f'Processing {deviceName}')

            # check for connected status entry in db
            connected_dev_from_db = Device_Model.find_by_status("connected")
            if connected_dev_from_db:
                if connected_dev_from_db.name != deviceName:
                    connected_dev_from_db.status = "disconnected"
                    connected_dev_from_db.save_to_db()
                    retDict["disconnected_device"] = connected_dev_from_db.json()

                    device = Device_Model.find_by_name(deviceName)
                    if device:
                        # Connecting existing device
                        device.status = "connected"
                    else:
                        # Adding a new device
                        device = Device_Model(deviceName, "connected")
                    device.save_to_db()
                    resp_status = status.HTTP_201_CREATED
                else:
                    resp_status = status.HTTP_202_ACCEPTED
            retDict["connected_device"] = device.json()  # create the body/payload

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Device_Disconnection_Resource(Resource):
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
                connected_dev_from_db = Device_Model.find_by_status("connected")  # check for connected status entry in db
                if (connected_dev_from_db != None) and (connected_dev_from_db.name == deviceName):
                    print(f"Disconnecting device {deviceName}")
                    connected_dev_from_db.status = "disconnected"   # Update db to disconnected status
                    connected_dev_from_db.save_to_db()
                    retDict["disconnected_device"] = connected_dev_from_db.json()
                    resp_status = status.HTTP_202_ACCEPTED
                else:
                    resp_status = HTTP_514_DB_ERROR = 514
                    error_str = ""
                    if connected_dev_from_db:
                        error_str = f"DB reports {deviceName} is {connected_dev_from_db.status}."
                    else:  # device isn't found in db
                        error_str = f"{deviceName} is not found in the {Device_Model.__tablename__} table."
                    print(error_str)
                    retDict["error_msg"] = error_str
            except Exception as error:
                resp_status = status.HTTP_503_SERVICE_UNAVAILABLE
                error_str = f"Unexpected error occurred. {error}"
                print(error_str)
                retDict["error_msg"] = error_str

        return Response(jsonify(retDict), status=resp_status, mimetype='application/json')

class Functional_Test_Resource(Resource):
    def post(self):
        pass

class PID_Command_Resource(Resource):
    def get(self):
        pass

    def post(self):
        """

        """
        pass

class Video_Feed_Resource(Resource):
    pass