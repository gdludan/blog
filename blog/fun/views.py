from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from blog_Plugin.robot import get_reply_free,get_reply_xiaoi
from blog_Plugin.music_163 import get_163MusicUrl
import requests,json
# Create your views here.
def chatfreeView(request):
    Open_source = True
    title = '菲菲'
    return render(request,'chat.html',locals())
def chatxiaoiView(request):
    Open_source = True
    title='小i'
    return render(request,'chat.html',locals())

def ajax_chat_free(request):
    res = {'status': 0, 'message': '未知错误','data':''}
    if request.is_ajax():
        data = get_reply_free(request.GET['data'])
        res['data'] = data
        res['message'] = 'successful'
        return JsonResponse(res)
    return JsonResponse(res)

def ajax_chat_xiaoi(request):
    res = {'status': 0, 'message': '未知错误','data':''}
    if request.is_ajax():
        data = get_reply_xiaoi(request.GET['data'])
        res['data'] = data.replace('\\r','').replace('\\t','').replace('\\n','')
        res['message'] = 'successful'
        return JsonResponse(res)
    return JsonResponse(res)

def musicView(request):
    Open_source = True
    mp3=True
    name=request.GET.get('name', '')
    redirecton = int(request.GET.get('redirect', '0'))
    website = request.GET.get('website', 'tencent').lower()
    if website == "netease".lower():
        if name:
            music_dict = get_163MusicUrl(name)
            value=music_dict['name']
            url = music_dict['url']
            if redirecton==2:
                return JsonResponse(music_dict)
            elif redirecton ==1:
                return redirect(url)
            else:
                return render(request, 'play.html', locals())
        else:
            name = "音乐"
            return render(request, 'play.html', locals())
    elif website =="tencent".lower():
        if name:
            music_dict = get_tencent(name)
            music_dict['picUrl'] = requests.get(music_dict['pic'], timeout=10).url
            value = music_dict['name']
            url = music_dict['url']
            if redirecton==2:
                return JsonResponse(music_dict)
            elif redirecton ==1:
                return redirect(url)
            else:
                return render(request, 'play.html', locals())
        else:
            name = "音乐"
            return render(request, 'play.html', locals())
    else:
        name = "音乐"
        return render(request, 'play.html', locals())

def videoView(request):
    Open_source = True
    url = request.GET.get('url','')
    name = '视频解析'
    return render(request,'play.html',locals())

def get_tencent(name=""):
    url = "https://api.bzqll.com/music/tencent/search?key=579621905&s=%s&limit=1&offset=0&type=song"%name
    data = json.loads(requests.get(url).text)
    if data["data"]:return data["data"][0]
    else:return {}