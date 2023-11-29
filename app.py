from flask import Flask
from flask import render_template
from flask import jsonify, request
import json, base64
import urllib.request
import requests
import time, math, datetime
import calendar
from bs4 import BeautifulSoup
import lxml

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
    if "url" in data:
     return rich_article_links(data['url'])
    else:
        return create_appts()

def add_repeat_time_slots(starttimelist, endtimelist):
    newstart = starttimelist[0]
    newend = endtimelist[0]
    dayiterations = 0

    while (newtime.weekday()!=0):
        newtime +=datetime.timedelta(days=1)
        dayiterations +=1
        
    for i in range(len(starttimelist)):
        newstart = starttimelist[i] + datetime.timedelta(days=dayiterations)
        starttimelist.append(newstart)
        newend = endtimelist[i] + datetime.timedelta(days=dayiterations)
        endtimelist.append(newend)
    return dayiterations
    
def rich_article_links(url):
     # data = json.loads(request.data)
     # url = data['url']
     page = requests.get(url)
     doc = page.content
     soup = BeautifulSoup(doc, "html.parser")
     title = soup.find("meta", property="og:title")["content"]
     image = soup.find("meta", property="og:image")["content"]
     output = {"title":title, "image":image}
     return (output)

def create_appts():
    data = json.loads(request.data)
    starttime = data['starttime'] 
    endtime = data['endtime']
    sessionduration = data['sessionduration']
    timebtwsessions = data['timebtwsessions']
    weekday_list = [data['mon'], data['tues'], data['wed'], data['thurs'], data['fri'], data['sat'], data['sun']]
    
    weekly = data['weekly']
    endrepeat = data['endrepeat']
    
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
        starttimelist[i] = starttimelist[i].strftime('20%y-%m-%dT%H:%M:%SZ')
        endtimelist[i] = datetime.datetime.fromtimestamp(int(endtimelist[i]))
        endtimelist[i] = endtimelist[i].strftime('20%y-%m-%dT%H:%M:%SZ')

    
    timeslotdictionary = dict(zip(starttimelist, endtimelist))
    
    headers = {"Authorization": "Bearer TOKEN", "Content-Type": "application/json"}
#    payload = {"End Appointment": "1702511107", "Start Time": "1702507507", "Available": "true"}
    url = "https://api.adalo.com/..."
    params = {"appID":"", "collectionID":""}

    output = []
#    for key, value in timeslotdictionary.items():
#        payload = {"End Appointment": value, "Start Appointment":key, "Name":"string", "Available": "true"}
#        payloadjson = json.dumps(payload)
#        response = requests.post(url, params=params, data = payloadjson, headers=headers)
#        time.sleep(.4)
    return (timeslotdictionary)


    
    
#    final_output = jsonify({"timeblocklength":blockduration, "minutes":blockminutes, "numberofslots":slotnumber})
#    output = json.dumps(timeslotdictionary)  
#    return output
 
#    headers = request.headers
#    auth = headers.get("Authorization")
#    if auth == 'hellodiana':
#        return jsonify({"message":"OK"}), 200
#    else:
#        return jsonify({"message":"Not Authorized"}), 400
    


