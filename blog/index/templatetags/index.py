from django import template
from blog import settings
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
        url = requests.get(
            "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7").json()['images']
        if not url:
            url = requests.get(
                "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7").json()['images']
        return strUrl + url[random.randint(0, len(url) - 1)]['url']
    except BaseException:
        return '/static/images/views.png'


@register.simple_tag(name='history_random')
# 历史名句
def history_random(local=0):
    url = 'https://api.tecchen.xyz/api/quote/history/random/'
    try:
        date = requests.get(url).json()['data']
        if not date:
            date = requests.get(url).json()['data']
        content, translation = date['content'], date['translation']
        return content if local == 1 else translation
    except BaseException:
        return '历史本身是自然史的一个现实的部分，是自然生成为人这一过程的一个现实的部分。——马克思'


@register.simple_tag(name='quote_random')
# 每日一句
def quote_random(local=0):
    url = 'https://api.tecchen.xyz/api/quote/'
    try:
        date = requests.get(url).json()['data']
        if not date:
            date = requests.get(url).json()['data']
        content, translation = date['content'], date['translation']
        return str(content if local == 1 else translation).replace("\n", '')
    except:
        return '历史的道路，不全是平坦的，有时走到艰难险阻的境界。这是全靠雄健的精神才能够冲过去的。——李道钊'


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
        return data[random.randint(0, len(data) - 2)]['title']
    try:
        return get_data()
    except BaseException:
        return "历史会重演。——修昔底德"


@register.simple_tag(name='replace')
def string_replace(string='archive', str1='archive', str2='存档'):
    return string.lower().replace(str1, str2)


@register.simple_tag(name='indexstatic')
def indexstatic(string=''):
    staticUrl = settings.STATIC_URL + string.replace('/static/', '', 1)
    if settings.oss:
        try:
            return str(settings.bucket.sign_url('GET', staticUrl[1:], 5 * 60)) .replace(
                '%2F', '/') if settings.bucket.object_exists(staticUrl) else staticUrl
        except BaseException:
            return staticUrl
    else:
        return staticUrl


@register.simple_tag(name='getDC')
def getDC(request):
    return request.scheme + "://" + request.META["HTTP_HOST"]


@register.simple_tag(name='getPath')
def getPath(request):
    return request.scheme + "://" + request.META["HTTP_HOST"] + request.path


@register.simple_tag(name='get_avatar')
def get_Avatar(user):
    try:
        if user.avatar == "/static/images/default.jpg":
            return "https://github.com/identicons/{}.png".format(user.get_username())
        else:
            return user.avatar
    except:
        return "https://github.com/identicons/guest.png"


@register.simple_tag(name='get_setting')
def get_setting(txt):
    from tools.models import SetCtarl
    data = SetCtarl.objects.filter(name=txt).first()
    return data.is_start if data.is_start else None


'''
自定义过滤器
@register.filter(name='cut')        {{ value | cut:'!' }}
自定义标签
@register.simple_tag(name='len')    {% len comment %}
'''
