import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys
from pprint import pprint
import numpy as np
from transliterate import translit

base_link = 'http://poincare.matf.bg.ac.rs/~kmiljan/raspored/sve/'

class Course:

    def __init__(self, description, day, teacher, start,
                 duration, course_type, groups, classroom, modules, years, subgroups):
        self.description = to_latin(description)
        self.day = day
        self.teacher = to_latin(teacher)
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.course_type = course_type
        self.groups = [(to_latin(group)).lower() for group in groups]
        self.classroom = to_latin(classroom)
        self.modules = [(to_latin(module)).lower() for module in modules]
        self.years = years
        self.subgroups = [to_latin(subgroup).lower() for subgroup in subgroups]

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.__dict__ == other.__dict__


def to_latin(text):
   return translit(text, 'sr', reversed=True)

def get_course(td, weekday, time, classroom):
    #convert course information to Course object
    text = str(td).strip()
    lines = text.split('\n')
    duration = int(td['colspan'])

    course_type = "lecture"

    if re.search(r'(вежбе)', text):
        course_type = "exercise"
    if re.search(r'(практикум)', text):
        course_type = "practicum"

    description = re.search(
            r'(?<=\>)[-a-zA-Z\u0400-\u04FF]+(\s[-a-zA-Z\u0400-\u04FF]+)*(\ \d[a-zA-Z\u0400-\u04FF]?)?', lines[0]).group(0)
    groups = list(
        set(re.findall(r'\d[a-zA-Z\u0400-\u04FF]+\d?[a-zA-Z\u0400-\u04FF]?', lines[1])))
    teacher = re.search(r'^(.*)?<', lines[-1]).group(0)[:-1]
    #subgroups = re.findall(r'(\u0413\u0420\d)', lines[2])
    subgroups = [x.strip() for x in lines[2].split(",")]

    modules = set([])

    for group in groups:
        for char in group:
            c = to_latin(char).lower()
            if c in "imnvrl":
                modules.add(c)
            if c == 'o':
                modules.update(list("mnvrl"))

    modules = list(modules)
    years = [int(group[0]) for group in groups]

    return Course(
        description,
        weekday,
        teacher,
        time,
        duration,
        course_type,
        groups,
        classroom,
        modules,
        years,
        subgroups
    )


def download_modules(courses):
    base = req.get(base_link)
    content = base.content.decode('utf-8')
    base_soup = BeautifulSoup(content, 'html.parser')

    groups = {x.get_text(): x['value'] for x in base_soup.find_all(
        'option', value=re.compile(r'form'))}

    groups.pop('СЕМИНАР')

    modules = {}
    # put groups under corresponding modules
    modules['i'] = [to_latin(x).lower() for x in groups.keys() if 'И' in x]
    modules['m'] = [to_latin(x).lower() for x in groups.keys() if 'М' in x or 'О' in x]
    modules['n'] = [to_latin(x).lower() for x in groups.keys() if 'Н' in x or 'О' in x]
    modules['v'] = [to_latin(x).lower() for x in groups.keys() if 'В' in x or 'О' in x]
    modules['r'] = [to_latin(x).lower() for x in groups.keys() if 'Р' in x or 'О' in x]
    modules['l'] = [to_latin(x).lower() for x in groups.keys() if 'Л' in x or 'О' in x]

    # put groups under corresponding years
    for x in modules.keys():
        years = {}
        for i in range(1, 6):
            years[i] = [group for group in modules[x] if group[0][0] == str(i)]
        modules[x] = years

    for module in modules:

        for year in modules[module]:

            courses_for_year = set([])

            for group in modules[module][year]:
                
                for course in courses:

                    if group in course['groups']:

                        courses_for_year.add(course['description'])

            courses_list = list(courses_for_year)
            courses_list.sort()
            modules[module][year] = courses_list

    return modules


def download_courses():
    # create instantiate all course objects
    base = req.get(base_link)
    content = base.content.decode('utf-8')
    base_soup = BeautifulSoup(content, 'html.parser')
    rooms = [(x['value'], x.get_text()) for x in base_soup.find_all(
        'option', value=re.compile(r'room'))]
    courses = []

    for room, room_name in rooms:

        print("Working on: " + room, file=sys.stderr)

        resp = req.get(base_link + room)
        content = resp.content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # for easier parsing
        for br in soup.find_all('br'):
            br.replace_with('\n')

        # rows = days
        rows = []
        rows.append(soup.find('td', {"bgcolor": re.compile(r".*")}).find_parent())
        rows.extend(rows[0].find_next_siblings('tr'))

        for i, row in enumerate(rows):

            time = 8

            # Pocinjemo od indeksa 1 jer preskacemo td sa radnim danom
            for td in row.find_all('td')[1::]:
                duration = 1
                if td.get_text().strip():
                    if not td.has_attr('colspan'):
                        td['colspan'] = 1
                    duration = int(td['colspan'])
                    courses.append(get_course(
                        td, i, time, room_name).__dict__)

                time += duration

    fix_disjoint(courses)

    return courses

def fix_disjoint(courses):
    courses.sort(key=lambda x: (x['day'], x['start']))
    #join courses that have only a room change
    for i, _ in enumerate(courses):
        j = i
        while j < len(courses) and courses[j]['start'] < courses[i]['end']:
            j += 1
        while j < len(courses) and courses[j]['start'] == courses[i]['end']:
            #if the only difference is the classroom
            if courses[j]['description'] == courses[i]['description']\
                and courses[j]['course_type'] == courses[i]['course_type']\
                and set(courses[j]['groups']) == set(courses[i]['groups'])\
                and set(courses[j]['subgroups']) == set(courses[i]['subgroups']):
                print("joining {} for {}".format(courses[i]['description'], courses[i]['groups']), file=sys.stderr)
                #then join
                courses[i]['end'] += courses[j]['duration']
                courses[i]['duration'] += courses[j]['duration']
                courses.pop(j)
            j += 1