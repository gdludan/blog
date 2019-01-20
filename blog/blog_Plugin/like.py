import requests
from bs4 import BeautifulSoup
def web_open(url,name):
    '''
    保存网络文件到硬盘
    :param url: 文件的url地址
    :param name: 写到硬盘的名字
    :return: 一个PIL.Image.Image.open对象
    '''
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    f = open(name, 'rb')
    return f
def Unicode_or_chinese(data):
    '''
    Unicode转UTF-8
    :param data: Unicode编码的字符串
    :return: 正常utf-8的字符串
    '''
    url="http://tool.chinaz.com/tools/unicode.aspx"
    data = {
        "content":data,
        "untoch":"Unicode 转 中文",
        "result":"",
    }
    cookies={
        "CNZZDATA5082706":"cnzz_eid%3D679896359-1545143002-null%26ntime%3D1547008318",
        "UM_distinctid":"167c1b32f6121c-03421404f09928-4d045769-100200-167c1b32f6220f",
        "qHistory":"aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy9jc3Nmb3JtYXQuYXNweCtDc3PmoLzlvI/ljJZ8aHR0cDovL2lwLnRvb2wuY2hpbmF6LmNvbStJUC/mnI3liqHlmajlnLDlnYDmn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy91bmljb2RlLmFzcHgrVW5pY29kZee8lueggei9rOaNog==",

    }

    html = requests.post(url,data=data,cookies=cookies).text
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find(class_ ="pr JsTxtW-r ml20 fl").textarea.get_text()
    return divs
