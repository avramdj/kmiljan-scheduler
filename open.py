import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys
from pprint import pprint
import pickle


courses = pickle.load(open('courses.p', 'rb'))
pprint(courses)