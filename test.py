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

