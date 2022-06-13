from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests


app = Flask(__name__)
imgurls = {'url':'text'}

def get_prediction(url):
    with urllib.request.urlopen(url) as URL:
        my_string=base64.b64encode(URL.read()).decode('utf-8')
    payload = {"instances":[{"image_bytes":{"b64":my_string},"key":"mykey"}]}
    jsonstring = json.dumps(payload)
    response = http.request('POST', 'https://curlpattern22-hjfqtyb23a-uc.a.run.app/v1/models/default:predict', fields=jsonstring)
    output = response.content
    return output

@app.route('/', methods =['GET', 'POST'])
def get_urls():
    update = {'url': request.json['url']}
    imgurls.update(update)
    newurl = imgurls.get('url')
    output = get_prediction(newurl)
    return output, 201

#@app.route("/", methods=['GET', 'POST'])
#def hello_world():
    #return render_template("index.html")
    #return "Hello There, Welcome To Your App!"
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    
   


