import requests
import json
import random
import re

header = [{'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'},
          {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
          {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
          {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'}, ]


def get_taobao_ipaddress(ip="0.0.0.0"):
    '''
    传入IP地址到淘宝 获取ip物理地址
    :param ip:IP网络地址
    :return:ip物理地址
    '''
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    request = requests.session()
    reque = request.get(
        url, headers=header[random.randint(0, len(header) - 1)]).text
    return json.loads(reque)


def get_360_ipaddres(ip="0.0.0.0"):
    '''
    传入IP地址到360 获取ip物理地址
    :param ip:IP网络地址
    :return:ip物理地址
    '''
    url = "https://www.so.com/s?q=%s" % ip
    request = requests.session()
    html = request.get(
        url, headers=header[random.randint(0, len(header) - 1)]).text
    text = re.compile(
        r'<p class="mh-detail ">.*?</span><span>(.*?)</span></p>')
    value = re.findall(text, html)
    if value == []:
        request = requests.session()
        html = request.get(
            url, headers=header[random.randint(0, len(header) - 1)]).text
        value = re.findall(text, html)
    return value[0].replace('&nbsp;', ' ').strip(' ')


def XX_remove(value=''):
    '''
    消除XX
    :param value:字符串内容
    :return: 当value不为xx时返回value，否则返回空字符串
    '''
    if value == '':
        return ''
    elif value == 'xx':
        return ''
    elif value == 'XX':
        return ''
    elif value == 'Xx':
        return ''
    elif value == 'xX':
        return ''
    else:
        return value
