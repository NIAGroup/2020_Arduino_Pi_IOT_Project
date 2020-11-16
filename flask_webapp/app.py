from flask import Flask, jsonify, request, redirect, render_template, Response
from camera import VideoCamera
import cv2
import sys

if sys.platform == 'win32':
     print("Running on Windows OS. This is not supported yet.")
     exit()

from src.device_list import BtDevContainer
Container = BtDevContainer()

app = Flask(__name__)

def gen_frames(camera):

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/")
def home():
    return render_template("index_new.html")

@app.route("/scan")
def scan():
    retDict = {}
    try:
        devices = Container.scan()
        retDict["scan_devs"] = devices
    except Exception as e:
        print(f"Runtime error has occurred. {e}")

    return jsonify(retDict)

@app.route('/video_feed')
def video_feed():
    print('Turn on Webcam')
    # return the response generated along with the specific  media
    # type (mime type)
    return Response(gen_frames(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0", port=5000, debug=True)
