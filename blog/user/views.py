from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from .forms import *
from django.db.models import Q
from index.models import Post
from user.models import Profile,Attention,Dynamic,MyUser as User
#from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from blog_Plugin.address import get_360_ipaddres
import random

#更换密码
@login_required(login_url='/user/login')
def passwdView(request):
    if request.method == 'POST':
        username = request.user.username
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
            if not user:
                tips = '原始密码错误'
            else:
                # 密码加密处理并保存到数据库
                user.password = make_password(new_password, None, 'pbkdf2_sha256')
                user.save()
                login(request, user)
                tips = '更改密码成功'
    return render(request,'passwd.html',locals())

#找回密码
def findPassword(request):
    button = '获取验证码'
    new_password = False
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
                tips = '验证码已发送'
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
                user = User.objects.filter(id = user[0].id).first()
                login(request,user)
                return redirect('/user/login')
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'findpassswd.html', locals())

def loginView(request):
    if request.user.is_authenticated :
        return redirect('/')
    form =CaptchaLoginForm()
    if request.method == 'POST':
        form,ip = CaptchaLoginForm(request.POST),''
        # 验证表单数据
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(Q(mobile=username) | Q(username=username)|Q(email=username)):
                user = User.objects.filter(Q(mobile=username) | Q(username=username)|Q(email=username)).first()
                if check_password(password, user.password):
                    # if request.META.has_key('HTTP_X_FORWARDED_FOR'):ip = request.META['HTTP_X_FORWARDED_FOR']
                    # else:ip = request.META['REMOTE_ADDR']
                    ip=request.META['REMOTE_ADDR']
                    user.ip=ip
                    user.ipaddress=get_360_ipaddres(user.ip)
                    user.save()
                    login(request, user)
                    tips = '登录成功'
                    return redirect(request.GET.get('next', '/'))
                else:
                    tips = '账号密码错误，请重新输入'
            else:
                tips = '用户不存在，请注册'
        else:
            tips = '验证码错误'
    return render(request, 'login.html', locals())

def registView(request):
    if request.user.is_authenticated :
        return redirect('/')
    form =CaptchaRegistForm()
    if request.method == 'POST':
        form = CaptchaRegistForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if not User.objects.filter(Q(username=username)|Q(email=email)):
                if password1 != password2:
                    tips = "两次密码不一致"
                else:
                    user = User(username=username,mobile='',email=email,
                              is_upload=0,avatar='/static/images/default.jpg',is_Auxiliary=0)
                    user.set_password(password2)
                    user.save()
                    profile = Profile(user=user,self_reprot=' 这个人很懒，什么也没有写！')
                    profile.save()
                    tips = '注册成功'
                    return redirect('/user/login')
            else:
                tips = '注册失败，用户已存在！'
        else:
            tips='验证码错误'
    return render(request, 'regist.html', locals())

def userView(request,username):
    page = request.GET.get('page',1)
    user_info = User.objects.filter(username=username).first()
    profile = Profile.objects.get(user=user_info)
    post_list = Post.objects.filter(user=user_info).order_by('-time').all()
    dynamic = Dynamic.objects.filter(user=user_info).first()
    if not dynamic:
        dynamic = Dynamic(user=user_info)
        dynamic.save()
    num_attention = dynamic.dynamic_attention
    attention_list = Attention.objects.filter(attention_id=user_info.id)
    if request.user.id:
        is_login = True
        for i in attention_list :
            if i.user == request.user and i.is_attention == 1: attention = 1
    else:
        is_login ,attention= False,0
    post_num = len(post_list)
    paginator = Paginator(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'user.html', locals())

@login_required(login_url='/user/login')
def homeView(request):
    user = User.objects.get(id = request.user.id)
    page = request.GET.get('page',1)
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile=Profile(user=user)
        profile.save()
    post_list = Post.objects.filter(user=user).order_by('-time').all()
    paginator = Paginator(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())

def logoutView(request):
    logout(request)
    return redirect('/')

# ajax接口，实现动态验证验证码
from django.http import JsonResponse
from captcha.models import CaptchaStore
def ajax_val(request):
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
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id=request.user.id)
        attention = Attention.objects.filter(user=user).first()
        user_info = User.objects.get(id=id)
        dynamic = Dynamic.objects.filter(user=user_info).first()
        if not attention:
            attention = Attention(user=user, attention_id=id,is_attention=0)
            attention.save()
        if not dynamic:
            dynamic = Dynamic(user=user_info)
            dynamic.save()
        if attention.is_attention == 1:
            attention.is_attention = 0
            if int(dynamic.dynamic_attention)>=1:
                dynamic.dynamic_attention = int(dynamic.dynamic_attention)-1
            res['status'] = 200
            res['message'] = '取消关注'
        else:
            attention.is_attention = 1
            dynamic.dynamic_attention = int(dynamic.dynamic_attention) + 1
            res['status'] = 200
            res['message'] = '关注成功'
        dynamic.save()
        attention.save()
        return JsonResponse(res)
    return JsonResponse(res)