# -*- coding: utf-8 -*-

import requests
import time
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
            school_num = re.search(regex, a.attrs['href'])
            if re.match('^\d+$', school_num.groups(0)[0]):
                school_name = a.string
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
            try:
                dept_num = int(dept_num.groups(0)[0])
                school_dept[dept_num] = {'name': dept.string, 'url': base_url + link.attrs['href']}
            except ValueError:
                pass

        school_dict[school_num]['depts'] = school_dept
        time.sleep(1)
    return school_dict


def get_class(base_url, school_dict):
    for school_num, school in school_dict.items():
        depts = school['depts']
        class_dict = {}
        for dept_num, dept in depts.items():
            class_dict[dept_num] = {}
            url = dept['url']
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            table = soup.find_all('table')[0]
            rows = table.find_all('tr')
            for _, tr_tag in enumerate(rows[3:]):
                td_list = tr_tag.find_all('td')
                try:
                    tds = [x for x in td_list]
                    num = tds[3].string
                    cat1 = tds[0].string
                    cat2 = tds[1].string
                    name = tr_tag.find('a').string
                    teacher = tr_tag.find(width='122').string

                    def grade_search(tr):
                        classes = [x for x in range(1, 8)]

                        for klass in classes:
                            tag = tr.find_all(class_='c' + str(klass) + 'm')
                            for text in tag:
                                if text.string and text.string != ' ':
                                    return klass

                    grade = grade_search(tr_tag)

                    class_dict[dept_num][num] = {'name': name,
                                                 'cat1': cat1,
                                                 'cat2': cat2,
                                                 'teacher': teacher.strip(),
                                                 'grade': grade}
                    school_dict[school_num]['depts'][dept_num]['classes'] = class_dict[dept_num]
                except IndexError:
                    pass
            time.sleep(1)
    return school_dict


def main():
    base_url = 'https://syllabus.kosen-k.go.jp'
    # school_dict = get_dept(base_url, get_school(base_url, {}))
    f = open('test.json', 'r')
    school_dict = json.load(f)
    school_dict = get_class(base_url, school_dict)
    print(json.dumps(school_dict, indent=2))


if __name__ == '__main__':
    main()
