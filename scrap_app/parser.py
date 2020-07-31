import requests
import codecs
from bs4 import BeautifulSoup as bsoup
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers =  [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
def work(url, city=None, language=None):
    jobs = []
    error = []
    # url = 'https://www.work.ua/jobs-kyiv-python/'
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = bsoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    cont = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'company': company, 'description': cont, 'url': domain+href, 'city_id': city, 'language_id': language})
            else:
                error.append({'url': url, 'title': 'Div does not exist'})
        else:
            error.append({'url': url, 'title': 'Page not found'})
    return jobs, error

def rabota(url, city=None, language=None):
    jobs = []
    error = []
    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = bsoup(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table', id='ctl00_content_ctl00_gridList')
                if table:
                    tr_list = table.find_all('tr', attrs={'id': True})
                    for tr in tr_list:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if dir:
                            title = div.find('p', attrs={'class': 'card-title'})
                            href = title.a['href']
                            cont = div.p.text
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                            jobs.append({'title': title.text, 'company': company, 'description': cont, 'url': domain+href, 'city_id': city, 'language_id': language})
                else:
                    error.append({'url': url, 'title': 'Table does not exist'})
            else:
                error.append({'url': url, 'title': 'Page is empty'})
        else:
            error.append({'url': url, 'title': 'Page not found'})
    return jobs, error

def dou(url, city=None, language=None):
    jobs = []
    error = []
    # domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = bsoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href']
                        # href = title.find('a', attrs={'class': 'vt'})['href']
                        cont = li.find('div', attrs={'class': 'sh-info'}).text
                        company = 'No name'
                        a = title.find('a', attrs={'class': 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text, 'company': company, 'description': cont, 'url': href, 'city_id': city, 'language_id': language})
            else:
                error.append({'url': url, 'title': 'Div does not exist'})
        else:
            error.append({'url': url, 'title': 'Page not found'})
    return jobs, error

def djinni(url, city=None, language=None):
    jobs = []
    error = []
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = bsoup(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_list:
                    # title = li.find('div',
                    #                 attrs={'class': 'list-jobs__title'})
                    # href = title.a['href']
                    # cont = li.find('div',
                    #                attrs={'class': 'list-jobs__description'})
                    # content = cont.text
                    # company = 'No name'
                    # comp = li.find('div',
                    #                attrs={'class': 'list-jobs__details__info'})
                    # if comp:
                    #     company = comp.text
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    # href = title.find('a', attrs={'class': 'vt'})['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'}).text
                    company = 'No name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text, 'company': company, 'description': cont, 'url': domain+href, 'city_id': city, 'language_id': language})

            else:
                error.append({'url': url, 'title': 'Div does not exist'})
        else:
            error.append({'url': url, 'title': 'Page not found'})
    return jobs, error

if __name__=='__main__':
    # url = 'https://jobs.dou.ua/vacancies/?city=%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2&category=Python'
    # jobs, error = dou(url)
    # h = codecs.open('dou.txt', 'w', 'utf-8')
    # for a in jobs:
    #     a = str(a)+'\n'
    #     h.write(a)
    # h.close()

    url = 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'
    jobs, error = djinni(url)
    h = codecs.open('djinni.txt', 'w', 'utf-8')
    for a in jobs:
        a = str(a)+'\n'
        h.write(a)
    h.close()


    # url = 'https://www.work.ua/jobs-kyiv-python/'
    # jobs, error = work(url)
    # h = codecs.open('work.txt', 'w', 'utf-8')
    # for a in jobs:
    #     a = str(a)+'\n'
    #     h.write(a)
    # h.close()

    # url = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=1'
    # jobs, error = rabota(url)
    # h = codecs.open('rabota.txt', 'w', 'utf-8')
    # for a in jobs:
    #     a = str(a)+'\n'
    #     h.write(a)
    # h.close()

    # h = codecs.open('work.html', 'w', 'utf-8')
    # h.write(str(resp.text))
    # h.close()
