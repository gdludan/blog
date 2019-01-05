import requests,re
from urllib.parse import quote

def get_reply_xiaoi(data):
    ini = "{'sessionId':'09e2aca4d0a541f88eecc77c03a8b393','robotId':'webbot','userId':'462d49d3742745bb98f7538c42f9f874','body':{'content':'" + data + "'},'type':'txt'}&ts=1529917589648"
    url = "http://i.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=" + quote(ini)
    cookie = {"cnonce": "808116", "sig": "0c3021aa5552fe597bb55448b40ad2a90d2dead5",
              "XISESSIONID": "hlbnd1oiwar01dfje825gavcn", "nonce": "273765", "hibext_instdsigdip2": "1"}
    r = requests.get(url, cookies=cookie)
    pattern = re.compile(r'\"fontColor\":0,\"content\":\"(.*?)\"')
    result = pattern.findall(r.text)
    arr=['真心听不懂你在说什么，要么你换种问法试试如何？','看不懂，大侠，能不能换个说法？？？','虽然小i读不懂你的话，但小i却能用心感受你对我的爱。']
    import random
    if len(result)>1:
        return result[1]
    else:
        return arr[random.randint(0,len(arr)-1)]

def get_reply_free(data):
    url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + data
    r = requests.get(url)
    result=r.text
    return result.lstrip('{"result":0,"content":"').rsplit('"}')[0]