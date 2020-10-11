from flask import Flask, jsonify, request, redirect, render_template
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_new.html")

@app.route("/scan")
def scan():
    devices = None
    error = None

    if sys.platform != 'win32':
        from src.device_list import BtDevContainer
        BtDevContainer()
        devices = BtDevContainer.scan()
    else:
        error = "Running on Windows OS. Most likely won't have any devices discovered."
        print(error)
    return render_template("index_new_scan.html", devices=devices, error=error)

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server, 
    # this allows users to get to the site by typing in the pi's
    # local ip address. 
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0", port=5000, debug=True)
