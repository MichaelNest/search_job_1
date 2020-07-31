import codecs
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_main.settings'
import django
django.setup()
from django.db import DatabaseError
from scrap_app.parser import *
from scrap_app.models import City, Language, Vacantion, Error, Url

User = get_user_model()

parsers = ((work, 'https://www.work.ua/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=1'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2&category=Python'),
           (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python')
           )

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, error = [], []

for func, url in parsers:
    j, e = func(url)
    jobs.append(j)
    error.append(e)

for job in jobs:
    for jb in job:
        # if jb != '\n\n':
        v = Vacantion(**jb, city=city, language=language)
        try:
            v.save()
        except DatabaseError:
            pass
if error:
    er = Error(data=error).save()
#
# f = codecs.open('jobs.txt', 'w', 'utf-8')
# for a in jobs:
#     a.append('\n')
#     for b in a:
#         b = str(b)+'\n'
#     # a = str(a)+'\n'
#     # f.write(a)
#         f.write(b)
# f.close()