import requests as req
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint
import pickle
import sys
from transliterate import translit


class Course:

    def __init__(self, description, day, teacher, start, duration, course_type, groups, classroom):

        self.description = to_latin(description)
        self.day = day
        self.teacher = to_latin(teacher)
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.course_type = course_type
        self.groups = to_latin(groups)
        self.classroom = to_latin(classroom)

    def __eq__(self, other): 
        if not isinstance(other, Course):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.__dict__ == other.__dict__


def to_latin(text):

    if isinstance(text, list):
        return [translit(x, 'sr', reversed=True) for x in text]
    return translit(text, 'sr', reversed=True)


def get_course(td, weekday, teacher, time):

    text = td.get_text().strip()
    duration = int(td['colspan'])

    course_type = "lecture"

    if re.search('(вежбе)', text):
        course_type = "exercise"
    if re.search('(практикум)', text):
        course_type = "practicum"

    description = re.search(
        '[a-z\u0400-\u04FF]+(\s[a-z\u0400-\u04FF]+)*(\ \d[a-z\u0400-\u04FF]?)?', text)
    description_pos = description.start()
    description_text = description.group(0)
    description = description.group(0)

    # Pomeramo text za ime predmeta, i zatim pretrazujemo odatle
    text = text[description_pos + len(description_text)::]

    groups = list(
        set(re.findall('\d[a-z\u0400-\u04FF]+\d?[a-z\u0400-\u04FF]?', text)))
    classroom = re.findall(
        '(?<=\()(\d{3}|[a-z\u0400-\u04FF]+\d*)(?=\))', text)[-1]

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


base_link = 'http://poincare.matf.bg.ac.rs/~kmiljan/raspored/sve/'
base = req.get(base_link)
content = base.content.decode('utf-8')
base_soup = BeautifulSoup(content, 'html.parser')

groups = {x.get_text(): x['value'] for x in base_soup.find_all(
    'option', value=re.compile('form'))}

# izbaci seminarski
groups.pop('СЕМИНАР')

modules = {}

# put groups under corresponding modules
modules['i'] = [(x, groups[x]) for x in groups.keys() if 'И' in x]
modules['m'] = [(x, groups[x]) for x in groups.keys() if 'М' in x or 'О' in x]
modules['n'] = [(x, groups[x]) for x in groups.keys() if 'Н' in x or 'О' in x]
modules['v'] = [(x, groups[x]) for x in groups.keys() if 'В' in x or 'О' in x]
modules['r'] = [(x, groups[x]) for x in groups.keys() if 'Р' in x or 'О' in x]
modules['l'] = [(x, groups[x]) for x in groups.keys() if 'Л' in x or 'О' in x]

# put groups under corresponding years
for x in modules.keys():

    years = {}

    for i in range(1, 6):

        years[i] = [group for group in modules[x] if group[0][0] == str(i)]

    modules[x] = years

# parse all course data from groups

forms = {}

for link in groups:



    forms[link] = pass


pprint(modules)
pickle.dump(modules, open('courses.p', 'wb'))