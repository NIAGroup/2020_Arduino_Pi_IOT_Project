from flask import Flask, jsonify, request, redirect, render_template
import sys
"""
if sys.platform == 'win32':
    print("Running on Windows OS. This is not supported yet.")
    exit()

from src.device_list import BtDevContainer
Container = BtDevContainer()
"""
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_new.html")

@app.route("/scan")
def scan():
    retDict = {}
    try:
        #devices = Container.scan()
        #retDict["scan_devs"] = devices
        retDict["scan_devs"] = ['test1', 'test2', 'test3', 'test4']
    except Exception as e:
        print(f"Runtime error has occurred. {e}")

    return jsonify(retDict)

@app.route("/connect", methods=['GET', 'POST'])
def connect():
    devices = request.get_json()
    print(devices)
    return jsonify({"selectedDevices": ["True", "True", "True", "True"]})


if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server, 
    # this allows users to get to the site by typing in the pi's
    # local ip address. 
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0", port=5000, debug=True)
