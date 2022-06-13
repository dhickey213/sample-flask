from flask import Flask
from flask import render_template
import sys
import pprint

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    output = pprint.pprint(sys.path)
    return output



   


