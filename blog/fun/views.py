from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from blog_Plugin.robot import get_reply_free,get_reply_xiaoi
from blog_Plugin.music import get_163MusicUrl,get_tencent
from blog_Plugin.images import get_img
from django.conf import settings
import requests,os
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

def ImageCompressionView(request):
    url = request.GET.get('url','')
    grade = int(request.GET.get('grade',2))
    redirecton = int(request.GET.get('redirect',0))
    name = "图片压缩"
    if url :
        if redirecton == 1:
            path = get_img(url, grade)
            img = open(path, 'rb')
            response = HttpResponse(img.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="' + path + '"'
            img.close()
            os.remove(settings.BASE_DIR+'/'+path)
            return response
        else:
            pathUrl = '/fun/images?redirect=1&grade=%s&url=%s'%(grade,url)
    return render(request, 'imagecompression.html', locals())
