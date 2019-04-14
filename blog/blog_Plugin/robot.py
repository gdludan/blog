import requests,re,json,random
from urllib.parse import quote

def get_reply_xiaoi(data):
    '''
    小i机器人
    :param data: 和机器人交谈的内容
    :return: 机器人的回答内容
    '''
    ini = "{'sessionId':'09e2aca4d0a541f88eecc77c03a8b393','robotId':'webbot','userId':'462d49d3742745bb98f7538c42f9f874','body':{'content':'" + data + "'},'type':'txt'}&ts=1529917589648"
    url = "http://i.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=" + quote(ini)
    cookie = {"cnonce": "808116", "sig": "0c3021aa5552fe597bb55448b40ad2a90d2dead5",
              "XISESSIONID": "hlbnd1oiwar01dfje825gavcn", "nonce": "273765", "hibext_instdsigdip2": "1"}
    r = requests.get(url, cookies=cookie)
    pattern = re.compile(u'\"fontColor\":0,\"content\":\"(.*?)\"')
    result = pattern.findall(r.text)
    arr=['真心听不懂你在说什么，要么你换种问法试试如何？','看不懂，大侠，能不能换个说法？？？',
         '虽然小i读不懂你的话，但小i却能用心感受你对我的爱。']
    if len(result)>1:
        return result[1]
    else:
        return arr[random.randint(0,len(arr)-1)]

def get_reply_free(data):
    '''
    菲菲机器人
    :param data: 和机器人交谈的内容
    :return: 机器人的回答内容
    '''
    url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + data
    result = json.loads(requests.get(url).text)
    return result['content']

from django.conf import settings

def get_reply_dandan(data):
    '''
    蛋蛋机器人
    :param data: 和机器人交谈的内容
    :return: 机器人的回答内容
    '''
    '''
    http://www.itpk.cn/     注册 api
    DANDANLOCAL = False  #拿到了api后设置成False
    DANDANAPIKEY = ""   #你的api key
    DANDANAPISECRET = ""  #你的 api secret
    '''
    if not settings.DANDANLOCAL:
        url="http://i.itpk.cn/api.php?question=%s&api_key=%s&api_secret=%s"\
            %(data,settings.DANDANAPIKEY,settings.DANDANAPISECRET)
    else:
        url="http://i.itpk.cn/api.php?question=%s"%data
    html = requests.get(url).text
    return html
