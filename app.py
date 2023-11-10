from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests
import time, math
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
    starttime = data['starttime']
    endtime = data['endtime']
    sessionduration = data['sessionduration']
    timebtwsessions = data['timebtwsessions']
    
    blockduration = float(endtime)-float(starttime)
    blockminutes = blockduration/60
    slotnumber = math.floor(blockminutes/(float(sessionduration) + float(timebtwsessions)))

    starttimelist = []
    endtimelist = []
    slotend = (sessionduration * 60)

    for i in range(slotnumber):
        starttimelist.append(starttime)
        endtimelist.append = (starttime + sessionduration)
        starttime = (starttime + sessionduration + timebtwsessions)

    timeslotdictionary = dict(zip(starttimelist, endtimelist))
    
#    final_output = jsonify({"timeblocklength":blockduration, "minutes":blockminutes, "numberofslots":slotnumber})
    output = jsonify(timeslotdictionary)   
    return output
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    


