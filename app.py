from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    #return render_template("index.html")
    a = 2
    print 'Hello There, Welcome To Your App!'
    exit()
