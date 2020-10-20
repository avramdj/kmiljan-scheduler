from flask import Flask
import json
import sys
import pickle
from pprint import pprint
from scheduler import Scheduler
from data_server import DataServer

app = Flask(__name__)
data = DataServer()

@app.route('/')
def hello():
    return data.get_modules()

@app.route('/i')#, methods=['GET', 'POST'])
def hello_world():
    return data.get_modules()['i']