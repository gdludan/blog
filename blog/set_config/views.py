from .forms import *
import os, blog,platform
from django.conf import settings
from index.models import Collection
from user.models import MyUser as User
from user.models import Profile,Attention
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='/user/login')
def edit_profileView(request):
    '''
    修改个人信息
    :param request: 客户端请求头
    :return: hrml页面
    '''
    form = ProfileForm()
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.filter(user=user).first()
    if not profile:profile=Profile(user=user,self_reprot='这个人很懒，什么也没有写！')#防止出现错误
    if request.method=='POST':
        profile.interest = request.POST.get('interest','')
        profile.aims = request.POST.get('aims','')
        profile.motto = request.POST.get('motto','')
        profile.self_reprot = request.POST.get('self_reprot','')
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name','')
        user.save()
        profile.save()
        tips = '修改个人信息成功'
    return render(request, 'edit_profile.html', locals())

@login_required(login_url='/user/login')
def edit_gravatarView(request):
    '''
    更改头像
    :param request: 客户端请求头
    :return: hrml页面
    '''
    file_url = request.user.avatar
    if request.method == 'POST':
        photo = request.FILES['photo']
        name= blog.randNmae() + os.path.splitext(photo.name)[1]
        photo_file = settings.MEDIA_ROOT+name
        with open(photo_file,'wb') as f:
            for fimg in photo.chunks():
                f.write(fimg)
        user = User.objects.filter(id = request.user.id).first()
        #删除以前的头像
        if platform.system() != 'Windows':os.system('rm -rf ' + settings.BASE_DIR+user.avatar)
        else:os.remove(settings.BASE_DIR+user.avatar)
        # UNIX和类UNIX(例如linux)系统会少四个字符
        if platform.system() !='Windows':str = 'stat'
        else:str =''
        user.avatar = '/'+ str +photo_file.lstrip(settings.BASE_DIR)
        user.save()
        tips= '上传头像成功'
    return render(request,'edit_gravatar.html',locals())

@login_required(login_url='/user/login')
def collection_managementView(request):
    '''
    收藏文章管理
    :param request: 客户端请求头
    :return: hrml页面
    '''
    title = '收藏的文章'
    page = request.GET.get('page',1)
    root_user = User.objects.get(id=request.user.id)
    collection_list = Collection.objects.filter(user=root_user).all()
    paginator = Paginator(collection_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request,'collection_manag.html',locals())

@login_required(login_url='/user/login')
def attention_managementView(request):
    '''
    关注博主管理
    :param request: 客户端请求头
    :return: hrml页面
    '''
    title = '关注的博主'
    page = request.GET.get('page',1)
    root_user = User.objects.get(id=request.user.id)
    attention_list = Attention.objects.filter(user=root_user).all()
    for i in attention_list:
        i.attention_id = User.objects.filter(id=i.attention_id).get()
    paginator = Paginator(attention_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request,'attention_manag.html',locals())
