#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import csv
from pprint import pprint

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

companies = []
search_requests = 'мотоцикл'

def optlist_parse(headers):
    page = 1
    base_url = 'https://optlist.ru/wholesales?page=' + str(page) + '&q=' + search_requests + '&saveQuery=true'
    
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, 'html.parser')
    divs1 = soup.find('p').text
    if request.status_code == 200:
        while divs1 != 'searchНичего не найдено по данному запросу':
            soup = bs(request.content, 'html.parser')
            divs = soup.find_all('div', attrs={'class': 'media-body'})
            #		print(divs)
            lendivs = soup.find_all('h2', attrs={'class': 'card__title-list'})
            for div in divs:
                try:
                    title = div.find('span', attrs={'itemprop': 'name'}).text
                    title2 = div.findAll('span', attrs={'class': 'text-md'})[1].text
                    hrefs = 'https://optlist.ru' + div.find('a')['href']
                    descriptions = div.find('p', attrs={'itemprop': 'description'}).text
                    companies.append({'title': title,
                                        'title2': title2,
                                        'hrefs': hrefs,
                                        'descriptions': descriptions})
                except:
                    pass
                
            page += 1
            base_url = 'https://optlist.ru/wholesales?page=' + str(page) + '&q=' + search_requests + '&saveQuery=true'
            request = session.get(base_url, headers=headers)
            divs1 = soup.find('p').text
        print(companies)
        print(len(companies))
    else:
        print('Error')
    return companies

optlist_parse(headers)

file1 = open('parser.csv', 'w', newline='')
a_pen = csv.writer(file1)
a_pen.writerow(('Title1', 'Title2', 'Описание', 'Ссылка'))
for company in companies:
    a_pen.writerow((company['title'], company['title2'], company['descriptions'], company['hrefs']))
