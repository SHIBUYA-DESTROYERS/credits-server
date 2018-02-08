# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json


def get_school(base_url, school_dict):
    url = base_url + '/Pages/PublicSchools'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    schools = soup.find_all('div', attrs={'class': 'btn btn-default'})
    for school in schools:
        a = school.find('a')
        regex = r'school_id=(\w+)'
        if a:
            school_name = a.string
            school_num = re.search(regex, a.attrs['href'])
            school_url = base_url + a.attrs['href']
            school_dict[school_num.groups(0)[0]] = {'name': school_name, 'url': school_url}
    return school_dict


def get_dept(base_url, school_dict):
    for school_num, school in school_dict.items():
        school_dept = {}
        url = school['url']
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        depts = soup.find_all('h4', attrs={'class': 'list-group-item-heading'})
        links = soup.find_all('a', text='本年度の開講科目一覧')
        regex = r'department_id=(\w+)'

        for link, dept in zip(links, depts):
            dept_num = re.search(regex, link.attrs['href'])
            school_dept[dept_num.groups(0)[0]] = {'name': dept.string, 'url': base_url + link.attrs['href']}

        school_dict[school_num]['depts'] = school_dept
    return school_dict


def main():
    base_url = 'https://syllabus.kosen-k.go.jp'
    school_dict = get_dept(base_url, get_school(base_url, {}))
    print(json.dumps(school_dict))


if __name__ == '__main__':
    main()
