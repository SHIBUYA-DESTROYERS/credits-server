# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

base_url = "https://syllabus.kosen-k.go.jp/Pages/PublicSchools"
r = requests.get(base_url)
soup = BeautifulSoup(r.content, 'lxml')

schools = soup.find_all("div", attrs={"class": "btn btn-default"})
for school in schools:
    a = school.find('a')
    if a:
        print(a.attrs['href'])
    print(school.text)