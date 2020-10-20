from flask import Flask
import json
import sys
import pickle
from pprint import pprint
from werkzeug.routing import BaseConverter
from scheduler import Scheduler
from data_server import DataServer

app = Flask(__name__)
data = DataServer()

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def hello():
    return data.get_modules()

@app.route('/api')
def api_root():
    return data.get_modules()

@app.route('/api/<regex("[imnvrl]"):uid>/')#, methods=['GET', 'POST'])
def api_smer(uid):
    return data.get_modules()[uid]


if __name__ == '__main__':
    app.run(host='localhost', port=3333)