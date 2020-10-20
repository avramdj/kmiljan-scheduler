import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys
from pprint import pprint
import pickle
import numpy as np


class Scheduler:

    def __init__(self, courses):

        self.bitmap = np.zeros(shape=(5, 13))
        self.placed = set([])
        self.courses = courses

    def find(self):

        if self._find(0):
            print(self.bitmap)
            return [json.loads(x) for x in self.placed]

    def _find(self, i):

        if i == len(self.courses):
            return True

        for term in self.courses[i][2]:

            if not self.conflict(term):
                self.place(term, i)

                if self._find(i+1):
                    return True
                
                self.remove(term)
        
        return False

    def conflict(self, term: dict):

        for i in range(term['start']-8, term['end']-8):

            if self.bitmap[term['day']][i] != 0:
                return True

        return False

    def place(self, term, j):

        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = j

        self.placed.add(json.dumps(term))

    def remove(self, term):

        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = 0

        self.placed.remove(json.dumps(term))
        
    def done(self):

        return len(self.placed) == len(self.courses)




all_courses = pickle.load(open('courses.p', 'rb'))
all_modules = pickle.load(open('modules.p', 'rb'))

module = input("Unesi module: ")
years = input("Godine iz kojih slusas kurseve: ").strip().split(" ")

courses = {}

i = 0

for year in years:

    g = int(year)

    for course in all_modules[module][g]:

        courses[i] = course
        i += 1

for (k, v) in courses.items():

    print(f'[{k}] {v}')

inds = input("Unesi indekse kurseva koje slusas: ").strip().split(' ')
picked = []

for ind in inds:
    picked.append([courses[int(ind)], 'lecture', 0])
    picked.append([courses[int(ind)], 'exercise', 0])

for i, _ in enumerate(picked):
    picked[i][2] = [x for x in all_courses if x['description'] == picked[i][0]
                                             and x['course_type'] == picked[i][1]]

#pprint(picked)

#print(picked[i])

scheduler = Scheduler(picked)
res = scheduler.find()
if res:
    res.sort(key=lambda x : (x['day'], x['start']))
    pprint(res)