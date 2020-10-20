import requests as req
from pprint import pprint
import pickle
from scheduler import Scheduler
from data_server import DataServer

data = DataServer()

all_courses = data.get_courses()
all_modules = data.get_modules()

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

pprint(picked)

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