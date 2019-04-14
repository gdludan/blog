from django import template
from blog_Plugin.todayInHistory import get_json
import requests
import random
register = template.Library()

@register.simple_tag(name='len')
# 过滤器在模板中使用时的name
def lenvalue(value):
    return str(len(value))

@register.simple_tag(name='requests_get')
def requests_Get(url):
    return requests.get(url).text


@register.simple_tag(name='requests_body')
def requests_body():
    strUrl = 'https://cn.bing.com'
    try:
        url = requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1").json()['images'][0]['url']
        if not url: url = \
        requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1").json()['images'][0]['url']
        for i in url:
            if i == '&':
                return strUrl
            else:
                strUrl += i
        return strUrl
    except:
        return '/static/images/views.png'


@register.simple_tag(name='history_random')
# 历史名句
def history_random(local=0):
    url='https://api.tecchen.xyz/api/quote/history/random/'
    date = requests.get(url).json()['data']
    if not date: date = requests.get(url).json()['data']
    content,translation = date['content'],date['translation']
    return content if local == 1 else translation



@register.simple_tag(name='quote_random')
# 每日一句
def quote_random(local=0):
    url='https://api.tecchen.xyz/api/quote/'
    date = requests.get(url).json()['data']
    if not date: date = requests.get(url).json()['data']
    content,translation = date['content'],date['translation']
    return content if local == 1 else translation


@register.simple_tag(name='today_in_History')
# 历史上的今天
def quote_random(str=''):
    temp = []

    def get_data():
        data = get_json()
        if str.lower() == 'all'.lower():
            for d in data:
                temp.append(d['title'])
            return temp
        return data[random.randint(0,len(data)-2)]['title']
    try:return get_data()
    except:return get_data()

@register.simple_tag(name='replace')
def string_replace(string='archive',str1='archive',str2='存档'):
    return string.lower().replace(str1,str2)

from blog import settings

@register.simple_tag(name='indexstatic')
def indexstatic(string=''):
    staticUrl = settings.STATIC_URL+string.replace('/static/', '')
    if settings.oss :
        try:
            return str(settings.bucket.sign_url('GET', staticUrl[1:], 5*60))\
                .replace('%2F','/') if settings.bucket.object_exists(staticUrl) else staticUrl
        except:
            return staticUrl
    else:
        return staticUrl

@register.simple_tag(name='getDC')
def getDC(request):
    return request.scheme +"://"+ request.META["HTTP_HOST"]

'''
自定义过滤器
@register.filter(name='cut')        {{ value | cut:'!' }}
自定义标签
@register.simple_tag(name='len')    {% len comment %}
'''