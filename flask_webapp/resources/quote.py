from flask import jsonify, redirect
from flask_restful import Resource, reqparse
import requests, json


class Quote(Resource):
    def get(self):

        url = 'https://api.forismatic.com/api/1.0/json?method=getQuote&lang=en&format=json'
        proxies = {'http':'http://proxy-us.intel.com:911', 'https':'http://proxy-us.intel.com:911'}
        params = {
            'method':'getQuote',
            'lang':'en',
            'format':'json'
        }
        resp = requests.get(url,params, proxies=proxies)
        print(resp.json())

        return resp.json()
