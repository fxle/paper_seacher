import os

import requests
from bs4 import BeautifulSoup

from downers.dblp_helper import down_all

down_root = 'down_pages'


def main_page_to_list(dblp_tip='https://dblp.uni-trier.de/db/journals/ijcv/', first_name='IJCV', second_name=''):
    # 返回对于这个主界面的子页面的东西
    # search_url_list [url, first_name , second_name ,year]
    search_url_list = []
    req = requests.get(url=dblp_tip)
    html = req.text
    bf = BeautifulSoup(html)

    ul_tag = bf.find_all('ul')[-6]  # 这个-6是实际的结果

    for li in ul_tag.find_all('li'):
        year = (li.contents[0]).split(':')[0]  # 去掉最后的东西
        for a in li.find_all('a'):
            url = a['href']
            search_url_list.append([url, first_name, second_name, year])

    return search_url_list


def write_to_txt(out_txt_path, search_url_list):
    f = open(out_txt_path, 'w')
    for items in search_url_list:
        f.write("%s,%s,%s,%s\n" % (items[0], items[1], items[2], items[3]))
    f.close()


def read_from_txt():
    txt_path = os.path.join(down_root, 'ijcv.txt')
    search_url_list = []
    if os.path.isfile(txt_path):
        f = open(txt_path, 'r')
        for line in f.readlines():
            items = line.split(',')
            search_url_list.append([items[0], items[1], items[2], items[3]])
    else:
        search_url_list = main_page_to_list()
        write_to_txt(txt_path, search_url_list)

    return search_url_list


if __name__ == '__main__':
    down_all(read_from_txt())
