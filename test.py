import requests as req
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint
import pickle
import sys
from transliterate import translit


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

# create forms dict so we don't iterate over the same form mulitple times

rooms = [(x['value'], x.get_text()) for x in base_soup.find_all(
    'option', value=re.compile('room'))]
courses = []

for room, room_name in rooms:

    print("Working on: " + room, file=sys.stderr)

    resp = req.get(base_link + room)
    content = resp.content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    # Odmah u startu uklanjamo sve <br> i pretvaramo u '\n' jer kasnije olaksava parsiranje
    for br in soup.find_all('br'):
        br.replace_with('\n')

    # Redovi (dani) glavne radne tabele
    rows = []
    rows.append(soup.find('td', {"bgcolor": re.compile(".*")}).find_parent())
    rows.extend(rows[0].find_next_siblings('tr'))

    # 5 Dana u radnoj nedelji
    for row_index in range(len(rows)):

        time = 8

        # Pocinjemo od indeksa 1 jer preskacemo td sa radnim danom
        for td in rows[row_index].find_all('td')[1::]:

            duration = 1
            if td.has_attr('colspan'):
                duration = int(td['colspan'])

                courses.append(get_course(
                    td, row_index, time, room_name).__dict__)

            time += duration

#pprint(courses)

for module in modules:

    for year in modules[module]:

        courses_for_year = set([])

        for group in modules[module][year]:
            
            for course in courses:

                if group in course['groups']:

                    courses_for_year.add(course['description'])

        modules[module][year] = courses_for_year

#pprint(modules)
pickle.dump(modules, open('modules.p', 'wb'))
pickle.dump(courses, open('courses.p', 'wb'))