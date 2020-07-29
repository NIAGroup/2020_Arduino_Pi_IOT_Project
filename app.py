from flask import Flask, jsonify, request, redirect, render_template
from flask_restful import Resource, Api

from resources.hello import HelloWorld
from resources.quote import Quote

import requests, json
import sqlite3

app = Flask(__name__)
api = Api(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

api.add_resource(Quote, '/quote')
api.add_resource(HelloWorld, '/greeting')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
