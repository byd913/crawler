#encoding=utf-8

''' 获取医院和医院科室的信息，然后保存到sqlite中
'''

import urllib
from bs4 import BeautifulSoup
import time
import sqlite3
import os

DB_PATH = '/home/xiaoju/data/hospital/hospital_info.db'


def get_total_pages():
    """ Get total number of page in hospital list page
    """
    html_doc = urllib.request.urlopen('http://www.bjguahao.gov.cn/hp.htm').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    total_pages = soup.find('input', attrs={'name': 'p_totalPage'})['value']
    return int(total_pages)


def get_hospital_ids(total_pages):
    hospital_dict = {}
    for page in range(1, total_pages+1):
        print('http://www.bjguahao.gov.cn/hp/%s,0,0,0.htm' % (page))
        html_doc = urllib.request.urlopen('http://www.bjguahao.gov.cn/hp/%s,0,0,0.htm' % (page)).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        info_list = soup.find_all('p', attrs={'class':'yiyuan_co_titl'})
        for info in info_list:
            name = info.a.string
            href = info.a['href']
            hospital_id = int(href.split('/')[-1].split('.')[0])
            href = 'http://www.bjguahao.gov.cn' + href
            hospital_dict[name] = {'hospital_id': hospital_id, 'href': href}
        time.sleep(1)
    return hospital_dict


def get_department_ids(hospital_id):
    department_dict = {}
    html_doc = urllib.request.urlopen('http://www.bjguahao.gov.cn/hp/appoint/1/%s.htm' % (hospital_id)).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    info_list = soup.find_all('a', attrs={'class': 'kfyuks_islogin'})
    for info in info_list:
        try:
            name = info.string
            href = info['href']
            department_id = int(href.split('-')[-1].split('.')[0])
            href = 'http://www.bjguahao.gov.cn' + href
            department_dict[name] = {'department_id': department_id, 'href': href}
        except:
            pass
    return department_dict


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    total_pages = get_total_pages()
    hospital_dict = get_hospital_ids(total_pages)

    for k, v in hospital_dict.items():
        print(k)
        cursor.execute('replace into hospital_info(hospital_id, name, href) values(%s, \'%s\', \'%s\')' 
                    % (v['hospital_id'], k, v['href']))
        department_dict = get_department_ids(v['hospital_id'])
        time.sleep(1)
        for dk, dv in department_dict.items():
            cursor.execute('replace into department_info(department_id, hospital_id, name, href) '
                        'values(%s, %s, \'%s\', \'%s\')' 
                        % (dv['department_id'], v['hospital_id'], dk, dv['href']))
    conn.commit()