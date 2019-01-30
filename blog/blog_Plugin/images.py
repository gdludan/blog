import PIL.Image as image
from PIL.Image import Image
from django.conf import settings
import requests,random,os,platform
def web_open_image(url,path,name,quality):
    '''
    保存网络图片到硬盘
    :param url: 图片的url地址
    :param name: 写到硬盘的名字
    :return: 一个PIL.Image.Image.open对象
    '''
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
    img = image.open(path)
    Image.save(img,name,quality=quality)
    os.remove(path)
    return name

def get_img(url,grade=2):
    '''
    压缩图片文件
    :param url: 图片的url地址
    :param grade: 压缩等级
    :return: 压缩后的文件名
    '''
    quality=[75,50,30,15]
    path = str(random.randint(10000,99999))+'.png'
    name = str(random.randint(1000,9999))+'.png'
    return web_open_image(url, path, name, quality[grade])
    # img = web_open_image(url,path,name,quality[grade])
    # # 删除图片文件
    # # os.remove(path)
    # return name