import random,time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def Sixteen():
    colorArr,color = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'],''
    for i in range(6):
        color += colorArr[random .randint(0,14)]
    return "#"+color

def RGB(red=[0,255],green=[0,255],blue=[0,255]):
    return (random.randint(red[0],red[1]),random.randint(green[0],green[1]),random.randint(blue[0],blue[1]))

def EN():
    colorArr=['Red', 'orange' ,'yellow' ,'green' ,'blue' ,'purple','White']
    return colorArr[random.randint(0, len(colorArr)-1)]

def randNmae():
    return str(round(time.time()* 1000))+str(random.randint(1000,9999))

def get_config(value,str=None):
    if value == None or value == '' or value==[] or value=={} or value == ():return str
    return value

def paginatorPage(data,page=10):
    paginator = Paginator(data, page)#分页
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        # 如果参数page的数据类型不是整型，则返回第一页数据
        pageInfo = paginator.page(1)
    except EmptyPage:
        # 用户访问的页数大于实际页数，则返回最后一页的数据
        pageInfo = paginator.page(paginator.num_pages)
    return paginator,pageInfo
import timeago,datetime
def timeago_or_time(date,str=False):
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    if str:return timeago.format(date=date,now=now,locale="zh_CN")
    else:return {'str':timeago.format(date=date,now=now,locale="zh_CN"),'data':date}

def timeago_not_time(date,str=False):
    now = datetime.datetime.now()
    if str: return timeago.format(date=date,now=now,locale="zh_CN")
    else:return {'str':timeago.format(date=date,now=now,locale="zh_CN"),'data':date}