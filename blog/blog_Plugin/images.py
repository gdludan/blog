import requests
import random
import os
from PIL import Image


def web_open_image(url, path, name):
    '''
    保存网络图片到硬盘
    :param url: 图片的url地址
    :param name: 写到硬盘的名字
    :return: 一个PIL.Image.Image.open对象
    '''
    r = requests.get(url, verify=False)
    with open(path, 'wb') as f:
        f.write(r.content)
    img = Image.open(path)
    img.thumbnail((img.size[0] / 1.6, img.size[1] / 1.6))
    img.save(name, quality=50)
    os.remove(path)
    return name


def get_img(url):
    '''
    压缩图片文件
    :param url: 图片的url地址
    :param grade: 压缩等级
    :return: 压缩后的文件名
    '''
    path = str(random.randint(10000, 99999)) + '.png'
    name = str(random.randint(10000, 99999)) + '.png'
    return web_open_image(url, path, name)
