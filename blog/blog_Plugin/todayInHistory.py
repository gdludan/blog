#! /usr/bin/python3
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
url = 'http://hao.360.cn/histoday/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) '
                  'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
request = requests.session()


def get_json():
    html = requests.get(url, headers=header)
    html.encoding = 'utf-8'
    html = html.text.replace('<em>', '').replace('</em>', '').replace('\n', '')
    soup = BeautifulSoup(html, 'html.parser')
    title_list = soup.find_all('dt')[1:]
    content_list = soup.find_all('div', {'class': 'desc'})
    temp = []
    num = 0
    for title in title_list:
        temp.append({'title': '', 'content': ''})
        temp[num]['title'] = title.get_text()[3:].replace(' ', '')
        num += 1
    num = 0
    for content in content_list:
        temp[num]['content'] = content.string.replace(' ', '')
        num += 1
    return temp
