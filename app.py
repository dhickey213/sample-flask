import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    #return render_template("index.html")
    response = requests.post('https://curlpattern22-hjfqtyb23a-uc.a.run.app/v1/models/default:predict', data={'url':'https://adalo-uploads.imgix.net/ee6ba0ead111d5deb1520f0ae2c4d9e2fd9831db5b8c1a544a7552ff9b186f5c.jpeg?orient'})
    output = response.content
    return "Hello There, Welcome To Your App!"

  
   


