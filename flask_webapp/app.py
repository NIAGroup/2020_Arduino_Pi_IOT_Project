from flask import Flask, jsonify, request, redirect, render_template
from src.device import Bt_Ble_Device
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_new.html")


if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server, 
    # this allows users to get to the site by typing in the pi's
    # local ip address. 
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    app.run(host="0.0.0.0",port=5000, debug=True)
