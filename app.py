from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return "hello diana!"



   


