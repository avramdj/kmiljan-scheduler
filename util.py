import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys
from pprint import pprint
import numpy as np
from transliterate import translit


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


class Course:

    def __init__(self, description, day, teacher, start,
                 duration, course_type, groups, classroom):
        self.description = to_latin(description)
        self.day = day
        self.teacher = to_latin(teacher)
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.course_type = course_type
        self.groups = [(to_latin(group)).lower() for group in groups]
        self.classroom = to_latin(classroom)

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.__dict__ == other.__dict__


def to_latin(text):
   return translit(text, 'sr', reversed=True)


def get_course(td, weekday, time, classroom):

    text = str(td).strip()
    lines = text.split('\n')
    duration = int(td['colspan'])

    course_type = "lecture"

    if re.search('(вежбе)', text):
        course_type = "exercise"
    if re.search('(практикум)', text):
        course_type = "practicum"

    description = re.search(
            '(?<=\>)[-a-zA-Z\u0400-\u04FF]+(\s[-a-zA-Z\u0400-\u04FF]+)*(\ \d[a-zA-Z\u0400-\u04FF]?)?', lines[0]).group(0)
    groups = list(
        set(re.findall('\d[a-zA-Z\u0400-\u04FF]+\d?[a-zA-Z\u0400-\u04FF]?', lines[1])))
    teacher = re.search('^(.*)?<', lines[-1]).group(0)[:-1]

    return Course(
        description,
        weekday,
        teacher,
        time,
        duration,
        course_type,
        groups,
        classroom
    )

