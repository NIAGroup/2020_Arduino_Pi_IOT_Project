import __init__
from flask import request, jsonify, render_template, Response, make_response, json
from flask_restful import Resource
from flask_api import status
from pprint import pprint
import time
from models.device_db_model import Device_Model, DB_RETURN_STATUS
from src.camera import VideoCamera, gen_frames

# Customize print
def custom_print(print_msg):
    pprint("***************************************************************************************")
    pprint(print_msg)
    pprint("***************************************************************************************")

print = custom_print

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

        print(retDict)

        return retDict, resp_status, headers

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
        retDict["scanned_devices"] = [
            {"name": 'test1', "status": 'disconnected'},
            {"name": 'test2', "status": 'disconnected'},
            {"name": 'test3', "status": 'disconnected'},
            {"name": 'test4', "status": 'disconnected'},
        ]

        print(retDict)

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

        print(retDict)

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
                resp_status, retDict, error_str = self._disconnect_dev_from_db(deviceName)
                if resp_status == status.HTTP_201_CREATED:  # Create a new db entry
                    resp_status, retDict, error_str = self._connect_dev_to_db(deviceName, retDict, resp_status)
            except Exception as error:
                resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_str = f"Unexpected error occurred. {error}"
                retDict["error_msg"] = error_str

        print(retDict)

        return retDict, resp_status, headers

class Device_Disconnection_Resource(Resource):
    def put(self):
        """
        Brief:
        Param(s):
        Return:
        """
        retDict = {}
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None

        devices = request.get_json()
        print(f'devices => {devices}')
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
                resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_str = f"Unexpected error occurred. {error}"
                retDict["error_msg"] = error_str

        print(retDict)

        return retDict, resp_status, headers

class Functional_Test_Resource(Resource):
    def post(self):
        retDict = {}
        retDict["function_tests"] = []
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None

        test_suite = request.get_json()
        print(f'{test_suite}')
        try:
            db_status, connected_dev_from_db = Device_Model.find_by_status("connected")
            if db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
                if connected_dev_from_db.name == test_suite["device"]:
                    resp_status = status.HTTP_200_OK
                    for func_test in test_suite["function_tests"]:
                        test_entry = {}
                        test_entry["name"] = func_test["name"]
                        test_entry["container_messages"] = []
                        for container_msg in func_test["container_messages"]:
                            msg = {}
                            msg["name"] = container_msg
                            msg["value"] = "Success"
                            test_entry["container_messages"].append(msg)
                        retDict["function_tests"].append(test_entry)
                else:
                    resp_status = DB_RETURN_STATUS["HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR"]
            else:
                resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        except Exception as error:
            resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_str = f"Unexpected error occurred. {error}"
            retDict["error_msg"] = error_str

        print(retDict)

        return retDict, resp_status, headers

class PID_Command_Resource(Resource):
    def post(self):
        retDict = {}
        headers = {"Content-type": "application/json; charset=UTF-8"}
        resp_status = None

        command_payload = request.get_json()
        print(f'{command_payload}')
        try:
            db_status, connected_dev_from_db = Device_Model.find_by_status("connected")
            if db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
                if connected_dev_from_db.name == command_payload["device"]:
                    resp_status = status.HTTP_200_OK
                    retDict["value"] = "Success"
                    retDict["btime"] = 12
                else:
                    resp_status = DB_RETURN_STATUS["HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR"]
            else:
                resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_str = f"Unexpected error occurred."
                retDict["error_msg"] = error_str
        except Exception as error:
            resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_str = f"Unexpected error occurred. {error}"
            retDict["error_msg"] = error_str

        print(retDict)

        return retDict, resp_status, headers

class Video_Feed_Resource(Resource):
    def __init__(self):
        self._cam = None

    def get(self):
        print('Turn on Webcam')
        if self._cam == None:
            self._cam = VideoCamera()
        else:
            time.sleep(0.1)
            if self._cam.isCameraActive:
                self._cam.isCameraActive = False
        return Response(gen_frames(self._cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')