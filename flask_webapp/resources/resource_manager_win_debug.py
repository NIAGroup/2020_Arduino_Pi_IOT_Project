import __init__
from flask import request, jsonify, render_template, Response, make_response, json
from flask_restful import Resource
from flask_api import status
from models.device_db_model import Device_Model, DB_RETURN_STATUS

class Home(Resource):
    def get(self):
        """

        """
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), status.HTTP_200_OK, headers)

class Previous_Connection_Resource(Resource):
    def get(self):
        """

        """
        resp_status = None
        headers = {"Content-type": "application/json; charset=UTF-8"}
        retDict = {'previously_paired_devices': [device.json() for device in Device_Model.query.all()]}
        if len(retDict['previously_paired_devices']) == 0:      # Check if db has any devices logged.
            resp_status = status.HTTP_404_NOT_FOUND
        else:
            resp_status = status.HTTP_200_OK

        return {'previously_paired_devices': [{"name":"you", "status":"disconnected"} , {"name":"me", "status":"connected"}]}, resp_status, headers

class Scanlist_Resource(Resource):
    def get(self):
        """
        Brief:
        Param(s):
        Return:
        """
        retDict = {}
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = status.HTTP_200_OK
        retDict["scanned_devices"] = ['test1', 'test2', 'test3', 'test4']

        return retDict, resp_status, headers

class Device_Connection_Resource(Resource):
    def _disconnect_dev_from_db(self, deviceName):
        resp_status = None
        retDict = {}
        error_str = ""
        db_status, connected_dev_from_db = Device_Model.find_by_status("connected")
        if db_status == DB_RETURN_STATUS["HTTP_200_OK"] or db_status == DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]:
            if db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
                if connected_dev_from_db.name == deviceName:  # If device already connected, don't do anything
                    resp_status = status.HTTP_202_ACCEPTED
                    retDict["connected_device"] = connected_dev_from_db.json()
                else:  # If different device connected, we'll create a new entry and disconnect previous
                    resp_status = status.HTTP_201_CREATED
                    connected_dev_from_db.status = "disconnected"
                    connected_dev_from_db.save_to_db()
                    retDict["disconnected_device"] = connected_dev_from_db.json()
            elif db_status == DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]:
                resp_status = status.HTTP_201_CREATED  # If no device connected, new entry is created
        elif db_status == DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
            error_str = f"Found multiple entries in the database with 'connected' status: {connected_dev_from_db}"
            resp_status = db_status
            retDict["error_msg"] = error_str

        return resp_status, retDict, error_str

    def _connect_dev_to_db(self, deviceName, retDict, resp_status):
        error_str = ""
        db_status, device = Device_Model.find_by_name(deviceName)
        if db_status != DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
            if device is not None:
                device.status = "connected"  # Change entry to connecting
            else:
                device = Device_Model(deviceName, "connected")  # Add a new device
            device.save_to_db()
            retDict["connected_device"] = device.json()
        else:
            error_str = f"Found multiple entries in the database with device name: {device.name}"
            resp_status = db_status
            retDict["error_msg"] = error_str

        return resp_status, retDict, error_str

    def get(self):
        """

        """
        retDict = {}
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None
        error_str = ""

        db_status, connected_dev_from_db = Device_Model.find_by_status("connected")
        if db_status == DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
            error_str = f"Found multiple entries in the database with 'connected' status: {connected_dev_from_db}"
            resp_status = db_status
            retDict["error_msg"] = error_str
        elif db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
            resp_status = status.HTTP_200_OK
            retDict["connected_device"] = connected_dev_from_db.json()
        else:   # DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]
            resp_status = status.HTTP_204_NO_CONTENT

        if error_str:
            print(error_str)

        return retDict, resp_status, headers

    def post(self):
        """

        """
        devices = request.get_json()
        print(f'devices => {devices}')
        retDict = {}
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None
        error_str = ""

        for deviceName in devices["selectedDevices"]:
            print(f'Processing {deviceName}')
            try:
                """
                # check for connected status entry in db
                status, connected_dev_from_db = Device_Model.find_by_status("connected")
                if status == DB_RETURN_STATUS["HTTP_200_OK"] or status == DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]:
                    if status == DB_RETURN_STATUS["HTTP_200_OK"]:
                        if connected_dev_from_db.name == deviceName:    # If device already connected, don't do anything
                            resp_status = status.HTTP_202_ACCEPTED
                            retDict["connected_device"] = connected_dev_from_db.json()
                        else:       # If different device connected, we'll create a new entry and disconnect previous
                            resp_status = status.HTTP_201_CREATED
                            connected_dev_from_db.status = "disconnected"
                            connected_dev_from_db.save_to_db()
                            retDict["disconnected_device"] = connected_dev_from_db.json()
                    elif status == DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]:
                        resp_status = status.HTTP_201_CREATED           # If no device connected, new entry is created
                """
                resp_status, retDict, error_str = self._disconnect_dev_from_db(deviceName)

                if resp_status == status.HTTP_201_CREATED:  # Create a new db entry
                    resp_status, retDict, error_str = self._connect_dev_to_db(deviceName, retDict, resp_status)
                    """
                    new_status, new_device = Device_Model.find_by_name(deviceName)
                    if new_status != DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
                        if new_device is not None:
                            new_device.status = "connected"     # Change entry to connecting
                        else:
                            new_device = Device_Model(deviceName, "connected")  # Add a new device
                        new_device.save_to_db()
                    else:
                        error_str = f"Found multiple entries in the database with device name: {new_device.name}"
                        resp_status = status
                        retDict["error_msg"] = error_str
                    """

            except Exception as error:
                resp_status = status.HTTP_503_SERVICE_UNAVAILABLE
                error_str = f"Unexpected error occurred. {error}"
                retDict["error_msg"] = error_str
                print(error_str)
                return retDict, resp_status, headers
        if error_str:
            print(error_str)

        return retDict, resp_status, headers

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
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None
        error_str = ""
        for deviceName in devices["selectedDevices"]:
            try:
                db_status, connected_dev_from_db = Device_Model.find_by_status("connected")
                if db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
                    if connected_dev_from_db.name == deviceName:
                        print(f"Disconnecting device {deviceName}")
                        connected_dev_from_db.status = "disconnected"  # Update db to disconnected status
                        connected_dev_from_db.save_to_db()
                        retDict["disconnected_device"] = connected_dev_from_db.json()
                        resp_status = status.HTTP_202_ACCEPTED
                    else:
                        error_str = f"DB reports {connected_dev_from_db.name} as the connected device instead of {deviceName}."
                        retDict["error_msg"] = error_str
                        resp_status = DB_RETURN_STATUS["HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR"]
                else:
                    if db_status == DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]:
                        error_str = f"{Device_Model.__tablename__} table returned no connected devices. {deviceName} not logged as connected."
                        retDict["error_msg"] = error_str
                        resp_status = db_status
                    elif db_status == DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
                        error_str = f"Found multiple entries in the database with connected status: {connected_dev_from_db}"
                        retDict["error_msg"] = error_str
                        resp_status = db_status
            except Exception as error:
                resp_status = status.HTTP_503_SERVICE_UNAVAILABLE
                error_str = f"Unexpected error occurred. {error}"
                retDict["error_msg"] = error_str
                print(error_str)
                return retDict, resp_status, headers

        if error_str:
            print(error_str)

        return retDict, resp_status, headers

class Functional_Test_Resource(Resource):
    def post(self):
        pass

class PID_Command_Resource(Resource):
    def get(self):
        pass

    def post(self):
        pass

class Video_Feed_Resource(Resource):
    pass