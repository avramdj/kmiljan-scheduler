import sys
import pickle
from pprint import pprint
from kmiljan_parser import download_courses, download_modules
from scheduler import Scheduler
from datetime import date

def fetch_courses():
    #fetch and periodically update course information
    all_courses = []
    all_modules = {}
    today = date.today().strftime("%b_%d_%Y")
    try:
        all_courses = pickle.load(open(f'pickles/courses_{today}.p', 'rb'))
        all_modules = pickle.load(open(f'pickles/modules_{today}.p', 'rb'))
    except FileNotFoundError:

        

        all_courses = download_courses()
        all_modules = download_modules(all_courses)

        pickle.dump(all_courses, open(f'pickles/courses_{today}.p', 'wb'))
        pickle.dump(all_modules, open(f'pickles/modules_{today}.p', 'wb'))

