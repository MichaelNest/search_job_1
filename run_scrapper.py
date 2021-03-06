import codecs
import asyncio
import os, sys


from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_main.settings'

import django
django.setup()

from scrap_app.parser import *
from scrap_app.models import City, Language, Vacantion, Error, Url

User = get_user_model()

# parsers = ((work, 'https://www.work.ua/jobs-kyiv-python/'),
#            (rabota, 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=1'),
#            (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2&category=Python'),
#            (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python')
#            )
parsers = ((work, 'work'),
           (rabota, 'rabota'),
           (dou, 'dou'),
           (djinni, 'djinni')
           )

jobs, error = [], []

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls

async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    error.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()
# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs.append(j)
#         error.append(e)
# for func, url in parsers:
#     j, e = func(url)
#     jobs.append(j)
#     error.append(e)

for job in jobs:
    for jb in job:
        # if jb != '\n\n':
        v = Vacantion(**jb)
        # v = Vacantion(**jb, city=city, language=language)
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