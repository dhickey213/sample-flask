from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests
import time, math, datetime
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

    sessionduration = (float(sessionduration) * 60)
    timebtwsessions = (float(timebtwsessions) * 60)
    starttime = float(starttime)

    for i in range(slotnumber):
        starttimelist.append(starttime)
        endtime_entry = (starttime + sessionduration)
        endtimelist.append(starttime + sessionduration)
        starttime = (starttime + sessionduration + timebtwsessions)

    for i in range(len(starttimelist)):
        starttimelist[i] = datetime.datetime.fromtimestamp(int(starttimelist[i]))
        starttimelist[i] = starttimelist[i].strftime('%y-%m-%dT%H:%M:%SZ')
        
    for i in range(len(endtimelist)):
        endtimelist[i] = datetime.datetime.fromtimestamp(int(endtimelist[i]))
        endtimelist[i] = endtimelist[i].strftime('%y-%m-%dT%H:%M:%SZ')
        
    timeslotdictionary = dict(zip(starttimelist, endtimelist))
    
    headers = {"Authorization": "Bearer 0dq63iciffzt986lb8g5it1ek", "Content-Type": "application/json"}
#    payload = {"End Appointment": "1702511107", "Start Time": "1702507507", "Available": "true"}
    url = "https://api.adalo.com/v0/apps/9dd54d7a-440a-494f-803f-acede8dff51e/collections/t_27kkg53ncepfrjhmjgdmmcupb"
    params = {"appID":"9dd54d7a-440a-494f-803f-acede8dff51e", "collectionID":"t_27kkg53ncepfrjhmjgdmmcupb"}

    output = []
    for key, value in timeslotdictionary.items():
        payload = {"Start Appointment": key, "End Appointment":value, "Available": "true"}
        payloadjson = json.dumps(payload)
        response = requests.post(url, params=params, data = payloadjson, headers=headers)
    #   output_me = json.loads(response.content)
    #    output.append(payload)
        time.sleep(.4)
   # print(output)
    return timeslotdictionary


    
#    final_output = jsonify({"timeblocklength":blockduration, "minutes":blockminutes, "numberofslots":slotnumber})
#    output = json.dumps(timeslotdictionary)  
#    return output
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    


