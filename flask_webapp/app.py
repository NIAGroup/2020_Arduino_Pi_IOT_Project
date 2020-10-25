from flask import Flask, jsonify, request, redirect, render_template
import sys

if sys.platform == 'win32':
    print("Running on Windows OS. This is not supported yet.")
    exit()

from src.device_list import BtDevContainer
Container = BtDevContainer()

app = Flask(__name__)

@app.route("/")
def home():
    """
    Brief:
    Param(s):
    Return:
    """
    return render_template("index_new.html")

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
        #retDict["scan_devs"] = ['test1', 'test2', 'test3', 'test4']
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
    retValue = {}
    for device in devices["selectedDevices"]:
        try:
            retValue[device] = Container.get_device(device).connect()
        except Exception:
            retValue[device] = False
    return jsonify(retValue)
    #print(devices)
    #return jsonify({"test2": True, "test3": True})

@app.route("/disconnect", methods=['GET', 'POST'])
def disconnect():
    """
    Brief:
    Param(s):
    Return:
    """
    devices = request.get_json()
    retValue = {}
    for device in devices["selectedDevices"]:
        try:
            Container.remove_device(device)
            retValue[device] = True
        except Exception:
            retValue[device] = False
    return jsonify(retValue)

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server, 
    # this allows users to get to the site by typing in the pi's
    # local ip address. 
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0", port=5000, debug=True)
