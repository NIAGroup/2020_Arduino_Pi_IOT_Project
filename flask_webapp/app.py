from flask import Flask
from flask_restful import Api
import sys
import atexit
#from db import db
from models.device_db_model import db, Device_Model
from src.camera import VideoCamera, gen_frames

if sys.platform == 'win32':
    print("Running on Windows OS. This is going to launch the debug version of this application.")
    from resources.resource_manager_win_debug import Home, Device_Connection_Resource, Device_Disconnection_Resource, \
        Scanlist_Resource, Previous_Connection_Resource, Functional_Test_Resource, PID_Command_Resource, Video_Feed_Resource
else:
    from resources.resource_manager import Home, Device_Connection_Resource, Device_Disconnection_Resource, \
        Scanlist_Resource, Previous_Connection_Resource, Functional_Test_Resource, PID_Command_Resource, Video_Feed_Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pid_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# -- This get's invoked when the application is getting closed -- #
def change_dev_status_to_disconnect_in_db():
    """
    doc: https://medium.com/better-programming/create-exit-handlers-for-your-python-appl-bc279e796b6b
    """
    with app.app_context():
        Device_Model.disconnect_all_devices()

atexit.register(change_dev_status_to_disconnect_in_db)

api.add_resource(Home, '/')
api.add_resource(Device_Connection_Resource, '/connect', endpoint='connect')
api.add_resource(Device_Disconnection_Resource, '/disconnect', endpoint='disconnect')
api.add_resource(Scanlist_Resource, '/scan', endpoint='scan')
api.add_resource(Previous_Connection_Resource, '/get_previously_paired', endpoint='get_previously_paired')
api.add_resource(Functional_Test_Resource, '/send_function_tests', endpoint='send_function_tests')
api.add_resource(PID_Command_Resource, '/send', endpoint='send')
#api.add_resource(Video_Feed_Resource, '/get_video_feed')

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)

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