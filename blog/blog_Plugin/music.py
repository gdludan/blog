import requests

def get_136Music(name=""):
    '''
    获取网易云歌曲详细信息调用接口
    :param name: 歌名
    :return: 歌曲详细信息的字典
    '''
    url = "https://api.bzqll.com/music/netease/search"
    params = {'key':579621905,'s':name,'limit':1,'offset':0,'type':'song'}
    data = requests.get(url,params=params).json()
    if data["data"]:
        data["data"][0]['pic']=requests.get(data["data"][0]['pic'], timeout=10).url
        data["data"][0]['url']=requests.get(data["data"][0]['url'], timeout=10).url
        data["data"][0]['lrc']=requests.get(data["data"][0]['lrc'], timeout=10).url
        return data["data"][0]
    else:return {}

def get_tencentMusic(name=""):
    '''
    获取腾讯歌曲详细信息
    :param name: 歌名
    :return: 歌曲详细信息的字典
    '''
    url = "https://api.bzqll.com/music/tencent/search"
    params = {'key':579621905,'s':name,'limit':1,'offset':0,'type':'song'}
    data = requests.get(url,params=params).json()
    if data["data"]:
        data["data"][0]['pic']=requests.get(data["data"][0]['pic'], timeout=10).url
        data["data"][0]['url']=requests.get(data["data"][0]['url'], timeout=10).url
        data["data"][0]['lrc']=requests.get(data["data"][0]['lrc'], timeout=10).url
        return data["data"][0]
    else:return {}
