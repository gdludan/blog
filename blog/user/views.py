import random
from .forms import CaptchaLoginForm,MyUserCreationForm
from index.models import Post
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from blog_Plugin.address import get_360_ipaddres
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
from user.models import Profile,Attention,Dynamic,MyUser as User
from django.contrib.auth.hashers import make_password,check_password
from blog import paginatorPage
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponse

def success(request):
    return HttpResponse('登录成功')

@login_required(login_url='/user/login')
def passwdView(request):
    '''
    更换密码
    :param request: 客户端请求头
    :return: html页面
    '''
    if request.method == 'POST':
        username = request.user.username
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
            if not user:messages.ERROR(request,'原始密码错误')
            else:
                # 密码加密处理并保存到数据库
                user.password = make_password(new_password, None, 'pbkdf2_sha256')
                user.save()
                login(request, user)
                messages.SUCCESS(request,'更改密码成功')
    return render(request,'passwd.html',locals(),RequestContext(request))

def findPassword(request):
    '''
    找回密码
    :param request: 客户端请求头
    :return: html页面
    '''
    button = '获取验证码'
    display = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            user = User.objects.filter(email=username)
        if not user:
            tips = '用户' + username + '不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                new_password = True
                VerificationCode = str(random.randint(100000, 999999))
                request.session['VerificationCode'] = VerificationCode
                msg = '你的用户名为：'+user[0].username+'\r\n验证码为：' + VerificationCode
                user[0].email_user('找回密码', msg)#发送邮件
                messages.success(request,'验证码已发送')
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                messages.success(request,'密码已重置')
                user = User.objects.filter(id = user[0].id).first()
                login(request,user)
                return redirect('/user/login')
            # 输入验证码错误
            else:
                messages.error(request,'验证码错误，请重新获取')
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'findpassswd.html', locals(),RequestContext(request))

def loginView(request):
    '''
    登录
    :param request: 客户端请求头
    :return: html页面,登录成功跳转首页
    '''
    if request.user.is_authenticated :return redirect('/')#已登录用户跳转到首页
    form =CaptchaLoginForm()
    if request.method == 'POST':
        form,ip = CaptchaLoginForm(request.POST),request.META['REMOTE_ADDR']
        # 验证表单数据
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(Q(mobile=username) | Q(username=username)|Q(email=username)):
                user = User.objects.filter(Q(mobile=username) | Q(username=username)|Q(email=username)).first()
                if check_password(form.cleaned_data['password'], user.password):#检查用户密码
                    user.ip=ip
                    # user.ipaddress=get_360_ipaddres(ip)#获取ip的物理地址
                    user.save()
                    login(request, user)
                    messages.success(request,'登录成功')
                    return redirect(request.GET.get('next', '/'))
                else:
                    messages.error(request,'账号或者密码错误，请重新输入')
            else:
                messages.error(request,'用户不存在，请注册')
        else:
            messages.error(request,'验证码错误')
    return render(request, 'login.html', locals(),RequestContext(request))

def registView(request):
    '''

    :param request: 客户端请求头
    :return: html页面,注册成功跳转登录页面
    '''
    if request.user.is_authenticated :return redirect('/')#已登录用户跳转到首页
    form =MyUserCreationForm()
    if request.method == 'POST':
        user = MyUserCreationForm(request.POST)
        if user.is_valid():#检查信息
            user.save()#添加新用户
            profile = Profile(user=user, self_reprot=' 这个人很懒，什么也没有写')#添加新用户的信息
            profile.save()
            messages.success(request,'注册成功')
            return redirect('/user/login')
        else:
            messages.error(request,'注册失败')
    return render(request, 'regist.html', locals(),RequestContext(request))

def userView(request,username):
    '''
    用户信息
    :param request: 客户端请求头
    :param username: 用户的id
    :return: html页面
    '''
    page = request.GET.get('page',1)
    user_info = User.objects.filter(username=username).first()
    profile = Profile.objects.get(user=user_info)
    post_list = Post.objects.filter(user=user_info).order_by('-time').all()
    dynamic = Dynamic.objects.filter(user=user_info).first()
    if not dynamic:dynamic = Dynamic(user=user_info);dynamic.save()
    num_attention = dynamic.dynamic_attention
    attention_list = Attention.objects.filter(attention_id=user_info.id).all()
    if request.user.id:
        is_login = True
        for i in attention_list :
            if i.user == request.user and i.is_attention == 1: attention = 1
    else:is_login ,attention= False,0
    num_fan = len(attention_list)
    post_num = len(post_list)
    paginator, pageInfo = paginatorPage(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    return render(request, 'user.html', locals(),RequestContext(request))

@login_required(login_url='/user/login')
def homeView(request):
    '''
    用户中心
    :param request: 客户端请求头
    :return: html页面
    '''
    user = User.objects.get(id = request.user.id)
    page = request.GET.get('page',1)
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile=Profile(user=user,self_reprot='这个人很懒，什么也没有写！')
        profile.save()
    post_list = Post.objects.filter(user=user).order_by('-time').all()
    attention_list = Attention.objects.filter(user=user).all()
    num_attentiom=len(attention_list)
    fan_list = Attention.objects.filter(attention_id=user.id).all()
    num_fan=len(fan_list)
    paginator, pageInfo = paginatorPage(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    return render(request, 'home.html', locals(),RequestContext(request))

def logoutView(request):
    '''
    注销登录
    :param request: 客户端请求头
    :return: html页面
    '''
    logout(request)
    messages.success(request, '注销成功')
    return redirect('/')

# ajax接口，实现动态验证验证码
from django.http import JsonResponse
from captcha.models import CaptchaStore
def ajax_val(request):
    '''
    检查码验证ajax接口
    :param request: 客户端请求数据
    :return: json数据
    '''
    if request.is_ajax():
        response = request.GET['response']# 用户输入的验证码结果
        hashkey = request.GET['hashkey']# 隐藏域的value值
        cs = CaptchaStore.objects.filter(response=response, hashkey=hashkey)# 若存在cs，则验证成功，否则验证失败
        if cs:json_data = {'status':1}
        else:json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        json_data = {'status':0}
        return JsonResponse(json_data)

def ajax_userattention(request,id):
    '''
    用户关注
    :param request:客户端请求数据
    :param id: 要关注用户的id
    :return:json数据
    '''
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id=request.user.id)
        attention = Attention.objects.filter(user=user,attention_id=id).first()
        dynamic = Dynamic.objects.filter(user=User.objects.filter(id=id).first()).first()
        if not dynamic:dynamic = Dynamic(user=User.objects.filter(id=id).first())#用户动态信息列表不存在就创建
        if not attention:attention = Attention(user=user, attention_id=id, is_attention=0)#用户关注列表不存在就创建
        if attention.is_attention ==1:
            attention.is_attention = 0
            if int(dynamic.dynamic_attention)>=1:dynamic.dynamic_attention = int(dynamic.dynamic_attention)-1#防止出现负数
            res['status'] = 200
            res['message'] = '取消关注'
        elif attention.is_attention ==0:
            attention.is_attention = 1
            dynamic.dynamic_attention = int(dynamic.dynamic_attention) + 1
            res['status'] = 200
            res['message'] = '关注成功'
        if dynamic.save() or attention.save():
            res['status'] = 401
            res['message'] = '写入数据库失败'
    return JsonResponse(res)