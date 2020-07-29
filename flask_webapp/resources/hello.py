from flask import jsonify, request, redirect, render_template
from flask_restful import Resource, reqparse
import requests, json


class HelloWorld(Resource):
    def get(self):
        return {'Hello':'World'}
