from django import template
from blog import timeago_or_time,timeago_not_time
import requests
register = template.Library()

@register.simple_tag(name='len')  # 过滤器在模板中使用时的name
def lenvalue(value):
    return str(len(value))

@register.simple_tag(name='timeago_or_time')  # 过滤器在模板中使用时的name
def timeagoOrTime(value,str=False,hours=8):
    return timeago_or_time(value,str=str,hours=hours)

@register.simple_tag(name='timeago_not_time')  # 过滤器在模板中使用时的name
def timeagoNotTime(value,str=False,hours=8):
    return timeago_or_time(value,str=str,hours=hours)

@register.simple_tag(name='requests_get')  # 过滤器在模板中使用时的name
def requests_Get(url):
    return requests.get(url).text

'''
自定义过滤器
@register.filter(name='cut')        {{ value | cut:'!' }}
自定义标签
@register.simple_tag(name='len')    {% len comment %}
'''