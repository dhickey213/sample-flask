from flask import Flask
from flask import render_template
import urllib3

app = Flask(__name__)


@app.route("/")
def hello_world():
    #return render_template("index.html")
    return "Hello There, Welcome To Your App!"

  
   


