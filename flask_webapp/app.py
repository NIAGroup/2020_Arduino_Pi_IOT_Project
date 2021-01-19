from flask import Flask, jsonify, request, redirect, render_template, Response
from flask_restful import Resource, Api
import sys, time

from db import db
from models.camera import VideoCamera, gen_frames
from resources.resource_manager import Home_Manager, Connection_Manager, Disconnection_Manager, Scanlist_Manager, \
    Previous_Connection_Manager, Functional_Test_Manager, PID_Command_Manager, Video_Feed_Manager

if sys.platform == 'win32':
    print("Running on Windows OS. This is not supported yet.")
    exit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pid_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

"""
outputFrame = None
cam = None
isCameraOn = False


@app.route("/send", methods=['GET', 'POST'])
def send():
    \"""
    Brief:
        send():
    POST:
        JSON => {selected_device_name : [ {method_name : {param_name : param_value} ] } ] }
    GET:
       JSON => {selected_device_name : {method_name : method_result} }
    \"""
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
"""
api.add_resource(Home_Manager, '/')
api.add_resource(Connection_Manager, '/connect')
api.add_resource(Disconnection_Manager, '/disconnect')
api.add_resource(Scanlist_Manager, '/scan')
api.add_resource(Previous_Connection_Manager, '/get_previously_paired')
api.add_resource(Functional_Test_Manager, '/send_function_tests')
api.add_resource(PID_Command_Manager, '/send')
api.add_resourece(Video_Feed_Manager, '/get_video_feed')

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
