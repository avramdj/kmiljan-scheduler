import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys
from pprint import pprint
import pickle
import numpy as np


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