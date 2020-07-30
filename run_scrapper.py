from scrap_app.parser import *
import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_main.settings'
import django
django.setup()

parsers = ((work, 'https://www.work.ua/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=1'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2&category=Python'),
           (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python')
           )

jobs, error = [], []

for func, url in parsers:
    j, e = func(url)
    jobs.append(j)
    error.append(e)

f = codecs.open('jobs.txt', 'w', 'utf-8')
for a in jobs:
    a.append('\n')
    for b in a:
        b = str(b)+'\n'
    # a = str(a)+'\n'
    # f.write(a)
        f.write(b)
f.close()