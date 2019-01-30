import os,platform
from django.conf import settings
from django.http import JsonResponse
from blog_Plugin.images import get_img
from blog_Plugin.like import Unicode_or_chinese
from django.shortcuts import render,redirect,HttpResponse
from blog_Plugin.music import get_163MusicUrl,get_tencent
from blog_Plugin.robot import get_reply_free,get_reply_xiaoi,get_reply_dandan
from django.template import RequestContext

# Create your views here.
def chatfreeView(request):
    '''
    菲菲聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title = '菲菲'
    return render(request,'chat.html',locals(),RequestContext(request))

def chatxiaoiView(request):
    '''
    小i聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title='小i'
    return render(request,'chat.html',locals(),RequestContext(request))

def chatdandanView(request):
    '''
    蛋蛋聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title='蛋蛋'
    return render(request,'chat.html',locals(),RequestContext(request))

def ajax_chat_free(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': u'未知错误','data':''}#定义错误信息
    if request.is_ajax():
        res['data'] = get_reply_free(request.GET['data'])#获取机器人返回的信息
        res['message'] = 'successful'
    return JsonResponse(res)

def ajax_chat_xiaoi(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': '未知错误','data':''}
    if request.is_ajax():
        res['data'] = get_reply_xiaoi(request.GET['data']).replace('\\r','').replace('\\t','').replace('\\n','')
        # 获取机器人返回的信息并删除一些不必要的符号
        res['message'] = 'successful'
    return JsonResponse(res)

def ajax_chat_dandan(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': u'未知错误','data':''}
    if request.is_ajax():
        getdata = request.GET['data']#获取传入的数据
        data = get_reply_dandan(getdata) # 获取机器人返回的信息
        if getdata == "笑话" or getdata == "观音灵签" or getdata == "月老灵签" or getdata == "财神爷灵签":
            data = Unicode_or_chinese(data)#字体转中文
        res['data'] = data
        res['message'] = 'successful'
    return JsonResponse(res)

def musicView(request):
    '''
    输入音乐名称，播放歌曲
    :param request: 客户端请求头
    :return: html页面或json数据
    '''
    mp3 = True#和video共享一个html文件
    #获取客户端请求的数据
    name=request.GET.get('name', '')#歌曲名字
    redirecton = int(request.GET.get('redirect', '0'))#放回数据类型
    website = request.GET.get('website', 'tencent').lower()#获取文件的
    if website == "netease".lower():
        if name:
            music_dict = get_163MusicUrl(name)#获取歌曲信息信息
            value=music_dict['name']
            url = music_dict['url']
            if redirecton==2:return JsonResponse(music_dict)#返回json数据
            elif redirecton ==1:return redirect(url)#跳转歌曲下载地址
        else:
            name = "音乐"
    elif website =="tencent".lower():
        if name:
            music_dict = get_tencent(name)#获取歌曲信息信息
            value = music_dict['name']
            url = music_dict['url']
            if redirecton==2: return JsonResponse(music_dict)#返回json数据
            elif redirecton ==1:return redirect(url)#跳转歌曲下载地址
        else:
            name = "音乐"
    return render(request, 'play.html', locals(),RequestContext(request))

def videoView(request):
    '''
    输入视频url播放视频
    :param request: 客户端请求头
    :return: html页面
    '''
    url = request.GET.get('url','')
    name = '视频解析'
    return render(request,'play.html',locals(),RequestContext(request))

def ImageCompressionView(request):
    '''
    输入图片url压缩图片
    :param request: 客户端请求头
    :return: html页面或跳转到压缩后的图片url
    '''
    #获取客户端请求的数据
    url = request.GET.get('url','')
    redirecton = int(request.GET.get('redirect',0))
    if url :
        if redirecton == 1:
            path = get_img(url, int(request.GET.get('grade',0)))#进行图片压缩
            img = open(path, 'rb')
            response = HttpResponse(img.read(), content_type='image/png')
            # response['Content-Disposition'] = 'attachment; filename="' + path + '"'
            img.close()
            # # 删除图片文件
            if platform.system() != 'Windows':os.system('rm -rf ' + settings.BASE_DIR + '/' + path)
            else:os.remove(path)
            return response
        else:
            pathUrl = '/fun/images?redirect=1&grade=%s&url=%s'%(request.GET.get('grade','0'),url)
    return render(request, 'imagecompression.html', locals(),RequestContext(request))
