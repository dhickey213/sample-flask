from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests
from time import datetime
import calendar

app = Flask(__name__)

def get_prediction(url):
    with urllib.request.urlopen(url) as URL:
        my_string=base64.b64encode(URL.read()).decode('utf-8')
    payload = {"instances":[{"image_bytes":{"b64":my_string},"key":"mykey"}]}
    jsonstring = json.dumps(payload)
    response = requests.post('https://curlpattern22-hjfqtyb23a-uc.a.run.app/v1/models/default:predict', data=jsonstring)
    output = json.loads(response.content)
    return output

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    data = json.loads(request.data)
    newurl = data['url']
    output = get_prediction(newurl)
    max_value= max(output['predictions'][0]['scores'])
    max_index= output['predictions'][0]['scores'].index(max_value)
    label_output= output['predictions'][0]['labels'][max_index]
    final_output = jsonify({"label":label_output})
    return final_output
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    


