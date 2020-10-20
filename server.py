from flask import Flask, jsonify, request
import sys
import pickle
from pprint import pprint
from scheduler import Scheduler

app = Flask(__name__)

@app.route('/')
def hello():
    return 'probaj /i /m /n /v /r /l'

@app.route('/i', methods=['GET', 'POST'])
def hello_world():
    return 