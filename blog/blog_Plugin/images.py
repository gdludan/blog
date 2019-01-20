import PIL.Image as image
from PIL.Image import Image
import requests,random,os
def web_open_image(url,name):
    '''
    保存网络图片到硬盘
    :param url: 图片的url地址
    :param name: 写到硬盘的名字
    :return: 一个PIL.Image.Image.open对象
    '''
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    img = image.open(name)
    return img

def get_img(url,grade):
    '''
    压缩图片文件
    :param url: 图片的url地址
    :param grade: 压缩等级
    :return: 压缩后的文件名
    '''
    quality=50
    if grade == 0: quality=90
    elif grade == 1: quality=70
    elif grade == 2: quality=50
    elif grade == 3: quality=30
    path = str(random.randint(10000,99999))+'.png'
    name = str(random.randint(1000,9999))+'.png'
<<<<<<< HEAD
    img = web_open_image(url,path)
=======
    img = web_open(url,path)
>>>>>>> aeeff182a610104a9cc0e7d9fc18f21768e53ee9
    Image.save(img,name, quality=quality)
    os.remove(path)
    return name
