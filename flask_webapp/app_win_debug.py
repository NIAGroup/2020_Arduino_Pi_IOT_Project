from flask import Flask, jsonify, request, redirect, render_template, Response
from flask_restful import Resource, Api
import sys

from db import db
from models.camera import VideoCamera, gen_frames
from resources.device import BluetoothDevice, Connect, Disconnect, DeviceList

# if sys.platform == 'win32':
     # print("Running on Windows OS. This is not supported yet.")
     # exit()

# from src.device_list import BtDevContainer
# Container = BtDevContainer()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pid_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# def gen_frames(camera):
#
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/")
def home():
    """
    Brief:
    Param(s):
    Return:
    """
    return render_template("index_new.html")

@app.route('/video_feed')
def video_feed():
    print('Turn on Webcam')
    # return the response generated along with the specific  media
    # type (mime type)
    return Response(gen_frames(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

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

api.add_resource(Connect, '/connect')
api.add_resource(Disconnect, '/disconnect')
api.add_resource(BluetoothDevice, '/scan')
api.add_resource(DeviceList, '/devices')

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
