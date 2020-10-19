import requests as req
from bs4 import BeautifulSoup
import re
import json
import sys

class Course:

        def __init__(self,description,day,teacher,start,duration,course_type,groups,classroom):
                
                self.description = description
                self.day = day
                self.teacher = teacher
                self.start = start
                self.duration = duration
                self.end = start + duration
                self.course_type = course_type
                self.groups = groups
                self.classroom = classroom

def get_course(td,weekday,teacher,time):

        text = td.get_text().strip()
        duration = int(td['colspan'])

        course_type = "lecture"

        if re.search('(вежбе)',text):
                course_type = "exercise"
        if re.search('(практикум)',text):
                course_type = "practicum"

        description = re.search('[a-z\u0400-\u04FF]+(\s[a-z\u0400-\u04FF]+)*(\ \d)?',text).group(0)

        groups = list(set(re.findall('\d[a-z\u0400-\u04FF]+\d?[a-z\u0400-\u04FF]?',text)))
        classroom = re.findall('(?<=\()(\d{3}|[a-z\u0400-\u04FF]+\d*)(?=\))',text)[-1]

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

# Main
base_link = 'http://poincare.matf.bg.ac.rs/~kmiljan/raspored/sve/'

resp = req.get(base_link)
content = resp.content.decode('utf-8')
bs_obj = BeautifulSoup(content,'html.parser')

# Dohvati sve profesore, mapiraj LINK -> IME
teachers = {x['value'] : x.get_text() for x in bs_obj.find_all('option',value=re.compile('teacher'))}
#pprint(teachers)

courses = []

for teacher in teachers.keys():
        
        print("Working on: " + teacher,file=sys.stderr)

        resp = req.get(base_link + teacher)
        content = resp.content.decode('utf-8')
        bs_obj = BeautifulSoup(content,'html.parser')

        # Odmah u startu uklanjamo sve <br> i pretvaramo u '\n' jer kasnije olaksava parsiranje
        for br in bs_obj.find_all('br'):
                br.replace_with('\n')

        # Redovi (dani) glavne radne tabele
        rows = []
        rows.append(bs_obj.find('td',{ "bgcolor" : re.compile(".*")} ).find_parent())
        rows.extend(rows[0].find_next_siblings('tr'))
        
        # 5 Dana u radnoj nedelji
        for row_index in range(len(rows)):
        
                time = 8
        
                # Pocinjemo od indeksa 1 jer preskacemo td sa radnim danom
                for td in rows[row_index].find_all('td')[1::]:
        
                        duration = 1
                        if td.has_attr('colspan'):
                                duration = int(td['colspan'])
        
                                courses.append(get_course(td,row_index,teachers[teacher],time))
        
        
                        time += duration
        
        
# Pretvori u json
print(json.dumps([ course.__dict__ for course in courses ],ensure_ascii=False))