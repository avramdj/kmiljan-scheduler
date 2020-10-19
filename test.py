import requests as req
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint
import sys


base_link = 'http://poincare.matf.bg.ac.rs/~kmiljan/raspored/sve/'
base = req.get(base_link)
content = base.content.decode('utf-8')
base_soup = BeautifulSoup(content, 'html.parser')

groups = [(x.get_text(), x['value']) for x in base_soup.find_all('option', value=re.compile('form'))]

# izbaci seminarski
groups.pop()

for group in groups.keys():

    print("Working on: " + group, file=sys.stderr)

    resp = req.get(base_link + group)
    content = resp.content.decode('utf-8')
    bs_obj = BeautifulSoup(content, 'html.parser')

    # Odmah u startu uklanjamo sve <br> i pretvaramo u '\n' jer kasnije olaksava parsiranje
    for br in bs_obj.find_all('br'):
        br.replace_with('\n')

    # Redovi (dani) glavne radne tabele
    rows = []
    rows.append(bs_obj.find('td', {"bgcolor": re.compile(".*")}).find_parent())
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
                    td, row_index, teachers[teacher], time))

            time += duration

modules = {}

#put groups under corresponding modules
modules['i'] = [x for x in groups if 'И' in x[0]]
modules['m'] = [x for x in groups if 'М' in x[0] or 'О' in x[0]]
modules['n'] = [x for x in groups if 'Н' in x[0] or 'О' in x[0]]
modules['v'] = [x for x in groups if 'В' in x[0] or 'О' in x[0]]
modules['r'] = [x for x in groups if 'Р' in x[0] or 'О' in x[0]]
modules['l'] = [x for x in groups if 'Л' in x[0] or 'О' in x[0]]

#put groups under corresponding years
for x in modules.keys():
    years = {}
    for i in range(1, 6):
        years[i] = [group for group in modules[x] if group[0][0] == str(i)]
    modules[x] = years

pprint(modules)

