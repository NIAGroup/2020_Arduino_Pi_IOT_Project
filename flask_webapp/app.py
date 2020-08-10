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
    return render_template("homepage.html")

@app.route("/home2")
def home2():
    return render_template("homepage_index_2.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

api.add_resource(Quote, '/quote')
api.add_resource(HelloWorld, '/greeting')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
