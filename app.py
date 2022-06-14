from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests

app = Flask(__name__)
imgurls = {'url':'text'}

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    data = json.loads(request.data)
    output = data['url']
    return output
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    


