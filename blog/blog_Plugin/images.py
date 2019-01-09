import PIL.Image as image
from PIL.Image import Image
import requests,random,os
def web_open(url,name):
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    img = image.open(name)
    return img

def get_img(url,grade):
    quality=50
    if grade == 0: quality=90
    elif grade == 1: quality=70
    elif grade == 2: quality=50
    elif grade == 3: quality=30
    path = str(random.randint(10000,99999))+'.png'
    name = str(random.randint(1000,9999))+'.png'
    img = web_open(url,path)
    Image.save(img,name, quality=quality)
    os.remove(path)
    return name
