import os
import platform
import threading
from .forms import *
import datetime
import pytz
import blog
import re
from index.models import Post
from blog import paginatorPage
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from blog_Plugin.images import get_img
from notifications.signals import notify
from index.views import get_notifications
from index.views import get_user, get_name
from django.template import RequestContext
from index.templatetags.index import getDC
from blog_Plugin.like import Unicode_or_chinese
from user.models import MyUser as User, UPfile, Attention
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from blog_Plugin.music import get_136Music, get_tencentMusic
from blog_Plugin.robot import get_reply_free, get_reply_xiaoi, get_reply_dandan


def sendNotify(request, user, post):
    attention_list = Attention.objects.filter(attention_id=user.id).all()
    for attention in attention_list:
        notify.send(
            get_notifications(),
            recipient=attention.user,
            level='info',
            verb='<a href="' +
            getDC(request) +
            '/post/' +
            str(
                post.id) +
            '">' +
            get_name(user) +
            '刚刚发布了《' +
            post.title +
            '》</a>')
    return 0


@login_required(login_url='/user/login')
def NewVisew(request):
    '''
    新建文章
    :param request: 客户端请求头
    :return: html页面或者跳转到主页
    '''
    form = PostForm()
    title__post = '发布文章'  # 按钮名称
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if re.match(r'<script>.*?</script>', request.POST.get('content', '')):
            messages.error(request, '发布文章失败，检测提交js脚本')
            return redirect('/user/home')
        post = Post(title=request.POST.get('title', ''),
                    content=request.POST.get('content', ''),
                    user=user, time=datetime.datetime.now())
        post.save()
        t = threading.Thread(target=sendNotify, args=(request, user, post))
        t.start()
        messages.error(request, '发布文章成功，检测提交js脚本')
        return redirect('/user/home')
    return render(request, 'post_file.html', locals(), RequestContext(request))


@login_required(login_url='/user/login')
def EidtorVisew(request, post_id):
    '''
    修改文章
    :param request: 客户端请求头
    :param post_id: 博客文章id
    :return: html页面或者跳转到主页
    '''
    form = PostForm()
    title__post = '确定修改'  # 按钮名称
    post = Post.objects.get(id=post_id)
    user = get_user(request)
    if user != post.user:
        return redirect('/')  # 判断当前用户是否为此文章作者
    if request.method == 'POST':
        if re.match(r'<script>.*?</script>', request.POST.get('content', '')):
            messages.error(request, '修改失败，检测提交js脚本')
            return redirect('/user/home')
        post.title = request.POST.get('title', '')
        post.content = request.POST.get('content', '')
        post.save()
        messages.success(request, '修改成功')
        return redirect('/user/home')
    return render(request, 'post_file.html', locals(), RequestContext(request))


@login_required(login_url='/user/login')
def UploadFileView(request):
    '''
    上传文件
    :param request: 客户端请求头
    :return: html页面
    '''
    user = User.objects.get(id=request.user.id)
    if user.is_upload == 0:
        return redirect('/')  # 检测用户上传权限
    form = UPfileForm()
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        file = request.FILES['file']
        name, filename = blog.randNmae() + '_' + file.name, file.name
        Upload_file, user = settings.MEDIA_ROOT_FILE + \
            name, User.objects.get(id=request.user.id)
        with open(Upload_file, 'wb') as f:
            for file_bytes in file.chunks():
                f.write(file_bytes)
        str = 'stat' if platform.system() != 'Windows'else ''  # UNIX和类UNIX(例如linux)系统会少四个字符
        upfile = UPfile(
            name=filename,
            file='/' +
            str +
            Upload_file.lstrip(
                settings.BASE_DIR),
            user=user,
            time=datetime.datetime.now(
                tz=pytz.timezone('UTC')))
        upfile.save()
        tips = '上传文件成功'
    upfile = UPfile.objects.filter(user=user).order_by('-time').all()
    post_num = len(upfile)
    paginator, pageInfo = paginatorPage(
        upfile, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    return render(
        request,
        'UploadFile.html',
        locals(),
        RequestContext(request))


def chatfreeView(request):
    '''
    菲菲聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title = '菲菲'
    return render(request, 'chat.html', locals(), RequestContext(request))


def chatxiaoiView(request):
    '''
    小i聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title = '小i'
    return render(request, 'chat.html', locals(), RequestContext(request))


def chatdandanView(request):
    '''
    蛋蛋聊天机器人
    :param request: 客户端请求数据
    :return: html页面
    '''
    title = '蛋蛋'
    return render(request, 'chat.html', locals(), RequestContext(request))


def ajax_chat_free(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': u'未知错误', 'data': ''}  # 定义错误信息
    if request.is_ajax():
        res['data'] = get_reply_free(request.GET['data'])  # 获取机器人返回的信息
        res['message'] = 'successful'
    return JsonResponse(res)


def ajax_chat_xiaoi(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': '未知错误', 'data': ''}
    if request.is_ajax():
        res['data'] = get_reply_xiaoi(
            request.GET['data']).replace(
            '\\r',
            '').replace(
            '\\t',
            '').replace(
                '\\n',
            '')
        # 获取机器人返回的信息并删除一些不必要的符号
        res['message'] = 'successful'
    return JsonResponse(res)


def ajax_chat_dandan(request):
    '''
    聊天机器人ajax
    :param request: 客户端请求信息
    :return: 一段json信息
    '''
    res = {'status': 0, 'message': u'未知错误', 'data': ''}
    if request.is_ajax():
        getdata = request.GET['data']  # 获取传入的数据
        data = get_reply_dandan(getdata)  # 获取机器人返回的信息
        if getdata == "笑话" or getdata == "观音灵签" or getdata == "月老灵签" or getdata == "财神爷灵签":
            data = Unicode_or_chinese(data)  # 字体转中文
        res['data'] = data
        res['message'] = 'successful'
    return JsonResponse(res)


def musicView(request):
    '''
    输入音乐名称，播放歌曲
    :param request: 客户端请求头
    :return: html页面或json数据
    '''
    mp3 = True  # 和video共享一个html文件
    # 获取客户端请求的数据
    name = request.GET.get('name', '')  # 歌曲名字
    redirecton = int(request.GET.get('redirect', '0'))  # 放回数据类型
    website = request.GET.get('website', 'tencent').lower()  # 获取文件的
    if website == "netease".lower():
        if name:
            music_dict = get_136Music(name)  # 获取歌曲信息信息
            if redirecton == 2:
                return JsonResponse(music_dict)  # 返回json数据
            elif redirecton == 1:
                return redirect(music_dict['url'])  # 跳转歌曲下载地址
    elif website == "tencent".lower():
        if name:
            music_dict = get_tencentMusic(name)  # 获取歌曲信息信息
            if redirecton == 2:
                return JsonResponse(music_dict)  # 返回json数据
            elif redirecton == 1:
                return redirect(music_dict['url'])  # 跳转歌曲下载地址
    return render(request, 'play.html', locals(), RequestContext(request))


def videoView(request):
    '''
    输入视频url播放视频
    :param request: 客户端请求头
    :return: html页面
    '''
    url = request.GET.get('url', '')
    name = '视频解析'
    return render(request, 'play.html', locals(), RequestContext(request))


def ImageCompressionView(request):
    '''
    输入图片url压缩图片
    :param request: 客户端请求头
    :return: html页面或跳转到压缩后的图片url
    '''
    # 获取客户端请求的数据
    url = request.GET.get('url', '')
    redirecton = int(request.GET.get('redirect', 0))
    if url:
        if redirecton == 1:
            path = get_img(url)  # 进行图片压缩
            img = open(path, 'rb')
            response = HttpResponse(img.read(), content_type='image/png')
            # response['Content-Disposition'] = 'attachment; filename="' + path + '"'
            img.close()
            os.remove(path)  # 删除图片文件
            return response
        else:
            pathUrl = '/fun/images?redirect=1&url={}'.format(url)
    return render(
        request,
        'imagecompression.html',
        locals(),
        RequestContext(request))
