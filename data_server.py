import sys
import os
from glob import glob
import pickle
from pprint import pprint
from kmiljan_parser import download_courses, download_modules
from scheduler import Scheduler
from datetime import date


class DataServer:
    
    def __init__(self):
        self.all_courses = []
        self.all_modules = {}
        self.last_update = None
        self.update()

    def get_courses(self):
        #fetch and periodically update course information
        today = date.today().strftime("%b_%d_%Y")
        
        if self.last_update != today:
            self.update()
        return self.all_courses

    def get_modules(self):
        #fetch and periodically update module information
        today = date.today().strftime("%b_%d_%Y")
        
        if self.last_update != today:
            self.update()
        return self.all_modules

    def update(self):
        self.all_courses = download_courses() #pickle.load(open('pickles/courses.p', 'rb')) 
        self.all_modules = download_modules(self.all_courses) #pickle.load(open('pickles/modules.p', 'rb'))

        #pickle.dump(self.all_courses, open('pickles/courses.p', 'wb'))
        #pickle.dump(self.all_modules, open('pickles/modules.p', 'wb'))

        today = date.today().strftime("%b_%d_%Y")
        self.last_update = today
