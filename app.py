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
import os


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
    elif "single_repeat_weekly" in data:
        return single_appt_repeat(data)
    else: 
        return (create_appts(data))


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

def single_appt_repeat(data):
    weekday_list = [data['mon'], data['tues'], data['wed'], data['thurs'], data['fri'], data['sat'], data['sun']]
    single_repeat_weekly = data['single_repeat_weekly']
  #  starttime = data['starttime'].replace("T"," ")
  #  starttime = starttime.replace("Z","")
  #  starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
    starttime = datetime.datetime.fromtimestamp(int(data['starttime']))
    endtime = datetime.datetime.fromtimestamp(int(data['endtime']))
  #  endtime = data['endtime'].replace("T"," ")
  #  endtime = endtime.replace("Z","")
  #  endtime = datetime.datetime.strptime(endtime, '%Y-%d-%m %H:%M:%S')
    endrepeat = datetime.datetime.fromtimestamp((int(data['endrepeat']))-604800)
    
    dayiterations = 0
    newstartlist = []
    newendlist = []
    nextstartday = starttime
    repeatstart = starttime
    repeatend = endtime
    nextendday = endtime

    for i in range(7):
        nextstartday += datetime.timedelta(days=1)
        nextendday += datetime.timedelta(days=1)
        dayiterations +=1
        if weekday_list[nextstartday.weekday()] == True:
            newstartlist.append(nextstartday)
            newendlist.append(nextendday)

#repeat weekly
    if single_repeat_weekly == True:
        while repeatstart < endrepeat:
            for i in range(len(newstartlist)):
                repeatstart = newstartlist[i] + datetime.timedelta(weeks=1)
                repeatend = newendlist[i] + datetime.timedelta(weeks = 1)
                newstartlist.append(repeatstart)
                newendlist.append(repeatend)
        
    for i in range(len(newstartlist)):
        newstartlist[i] = newstartlist[i].strftime('20%y-%m-%dT%H:%M:%SZ')
        newendlist[i] = newendlist[i].strftime('20%y-%m-%dT%H:%M:%SZ')

    
    single_repeat_week_dict = dict(zip(newstartlist, newendlist))
    
 #app vars   
    a_token = "Bearer " + os.environ['token']
    app_url = os.environ['app_url']
    appID = os.environ['appID']
    collectionID = os.environ['collectionID']
    
    headers = {"Authorization": a_token, "Content-Type": "application/json"}
#   payload = {"End Appointment": "1702511107", "Start Time": "1702507507", "Available": "true"}
#    url = "https://api.adalo.com/..."
    params = {"appID":appID, "collectionID":collectionID}

#    output = []
    for key, value in single_repeat_week_dict.items():
        payload = {"End Appointment": value, "Start Appointment":key, "Name":"", "Available": "true"}
        payloadjson = json.dumps(payload)
        response = requests.post(app_url, params=params, data = payloadjson, headers=headers)
        time.sleep(.2)

    output = jsonify ({"starttime": str(data['starttime']), "endtime": str(data['endtime'])})
    output2 = jsonify(single_repeat_week_dict)
    return (output2)
    

def create_appts(data):
    #data = json.loads(request.data)
    starttime = data['starttime'] 
    endtime = data['endtime']
    sessionduration = data['sessionduration']
    timebtwsessions = data['timebtwsessions']
    weekday_list = [data['mon'], data['tues'], data['wed'], data['thurs'], data['fri'], data['sat'], data['sun']]
    weekly = data['weekly']
    endrepeat = data['endrepeat']


    # Create day 1 time slots   
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
        endtimelist[i] = datetime.datetime.fromtimestamp(int(endtimelist[i]))
        
# Create Time Slots for Week 1
    newstart = starttimelist[0]
    newend = endtimelist[0]
    next_day = starttimelist[0]
    dayiterations = 0
    newstartlist = []
    newendlist = []

    for i in range(6):
        next_day += datetime.timedelta(days=1)
        dayiterations +=1
        if weekday_list[next_day.weekday()] == True:
            for i in range(len(starttimelist)):
                newstart = starttimelist[i] + datetime.timedelta(days=dayiterations)
                newstartlist.append(newstart)
                newend = endtimelist[i] + datetime.timedelta(days=dayiterations)
                newendlist.append(newend)

#Add week 1 slots to day 1 slots
    starttimelist.extend(newstartlist)
    endtimelist.extend(newendlist)

#Add Repeat Weekly dates
    if weekly == True:
        endrepeat = datetime.datetime.fromtimestamp((int(endrepeat))-604800)
        startweekly = starttimelist[0]
        endweekly = endtimelist[0]
        startweeklylist = []
        endweeklylist = []
        weeklyloop = 0
    
        while startweekly < endrepeat and weeklyloop<9:
            weeklyloop += 1
            for i in range(len(starttimelist)):
                startweeklylist.append(starttimelist[i] + datetime.timedelta(weeks=weeklyloop))
                endweeklylist.append(starttimelist[i] + datetime.timedelta(weeks=weeklyloop))
            
                

        starttimelist.extend(startweeklylist)
        endtimelist.extend(endweeklylist)
    
    for i in range(len(starttimelist)):
        starttimelist[i] = starttimelist[i].strftime('20%y-%m-%dT%H:%M:%SZ')
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
    


