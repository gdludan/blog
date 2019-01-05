import requests,json

def get_163url(id):
    url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % id
    headers = {'Accept': '*/*','Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    return requests.get(url, headers=headers, timeout=10).url

def get_163MusicUrl(music=''):
    if music:
        url = 'http://s.music.163.com/search/get?'
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        dataMusic = {'type': '1','s': music,'limit':2,'offset': 0}
        r = json.loads(requests.get(url,params=dataMusic,headers=headers).text)['result']['songs'][0]
        music_dict={'name':r['name'],'artists':r['artists'][0]['name'],'artists_id':r['artists'][0]['id'],
                    'album':r['album']['name'],'album_id':r['album']['id'],'picUrl':r['album']['picUrl'],
                    'page':r['page'],'url':'',}
        music_dict['url'] = get_163url(r['id'])
        return music_dict
        # return {'url': ''}
    else:return {'url':''}
# print(get_163MusicUrl('你好'))