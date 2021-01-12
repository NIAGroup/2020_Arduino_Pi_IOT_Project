from flask import Flask, jsonify, request, redirect, render_template, Response 
from camera import *
import cv2, time
import sys

if sys.platform == 'win32':
     print("Running on Windows OS. This is not supported yet.")
     exit()

from src.device_list import BtDevContainer
Container = BtDevContainer()

outputFrame = None
cam = None
isCameraOn = False

app = Flask(__name__)

@app.route("/")
def home():
    """
    Brief:
    Param(s):
    Return:
    """
    return render_template("index.html")

@app.route("/scan")
def scan():
    """
    Brief:
    Param(s):
    Return:
    """
    retDict = {}
    try:
        devices = Container.scan()
        retDict["scan_devs"] = devices
    except Exception as e:
        print(f"Runtime error has occurred. {e}")

    return jsonify(retDict)

@app.route("/connect", methods=['GET', 'POST'])
def connect():
    """
    Brief:
    Param(s):
    Return:
    """
    devices = request.get_json()
    retValue = {"connectedDevice": {}}
    for device in devices["selectedDevices"]:
        try:
            retValue["connectedDevice"][device] = Container.get_device(device).connect()
            #Todo: Update db to connected status
        except Exception:
            retValue["connectedDevice"][device] = False
    return jsonify(retValue)

@app.route("/disconnect", methods=['GET', 'POST'])
def disconnect():
    """
    Brief:
    Param(s):
    Return:
    """
    devices = request.get_json()
    retValue = {"disconnectedDevice": {}}
    for device in devices["selectedDevices"]:
        try:
            Container.get_device(device).disconnect()
            # Todo: Update db to disconnected status.
            retValue["disconnectedDevice"][device] = True
            retValue[device] = True
        except Exception as error:
            print(f"Unexpected error occurred. {error}")
            retValue["disconnectedDevice"][device] = False
    return jsonify(retValue)

@app.route("/send", methods=['GET', 'POST'])
def send():
    """
    Brief:
        send():
    POST:
        JSON => {selected_device_name : [ {method_name : {param_name : param_value} ] } ] }
    GET:
       JSON => {selected_device_name : {method_name : method_result} }
    """
    devices = request.get_json()
    retValue = {}
    for device_name in devices["selectedDevices"]:
        retValue[device_name] = {}
        for msg_name in devices[device_name]:
            print(f"Sending command: {msg_name} params: {devices[device_name][msg_name]}")
            try:
                retValue[device_name][msg_name] = Container.get_device(device_name).send_message(msg_name, **devices[device_name][msg_name])
            except Exception:
                print(f"Unexpected error occurred upon sending command: {msg_name}. Returning False.\n{Exception}")
                retValue[device_name][msg_name] = False

    return jsonify(retValue)

@app.route('/video_feed')
def video_feed():
    print('Turn on Webcam')
    # return the response generated along with the specific  media
    # type (mime type)
    global cam
    global isCameraOn
    if cam == None:
        cam = VideoCamera()
        isCameraOn = True
    else:
        time.sleep(0.1)
        if cam.isCameraActive:
            cam.isCameraActive = False
    return Response(gen_frames(cam),
        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0", port=5000, debug=True)
