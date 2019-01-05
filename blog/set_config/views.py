from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from user.models import MyUser as User
import os, blog
from .forms import *
from index.models import Post,Comment,Collection
from user.models import Profile,Attention
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='/user/login')
def edit_profileView(request):
    form = ProfileForm()
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    if request.method=='POST':
        profile.interest = request.POST.get('interest','')
        profile.aims = request.POST.get('aims','')
        profile.motto = request.POST.get('motto','')
        profile.self_reprot = request.POST.get('self_reprot','')
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name','')
        email=request.POST.get('email','')
        user.save()
        profile.save()
        tips = '修改个人信息成功'
    return render(request, 'edit_profile.html', locals())

@login_required(login_url='/user/login')
def edit_gravatarView(request):
    file_url = request.user.avatar
    if request.method == 'POST':
        photo = request.FILES['photo']
        name= blog.randNmae() + os.path.splitext(photo.name)[1]
        photo_file = '%s%s'%(settings.MEDIA_ROOT,name)
        with open(photo_file,'wb') as f:
            for fimg in photo.chunks():
                f.write(fimg)
        user = User.objects.filter(id = request.user.id).first()
        acatar = settings.BASE_DIR+user.avatar
        import platform
        str =''
        if platform.system() !='Windows':
            str = 'stat'
        user.avatar = '/'+ str +photo_file.lstrip(settings.BASE_DIR)
        user.save()
        os.remove(acatar)
        tips= '上传头像成功'
        file_url = user.avatar
    return render(request,'edit_gravatar.html',locals())

@login_required(login_url='/user/login')
def collection_managementView(request):#收藏文章管理
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
def attention_managementView(request):#关注博主管理
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

# from django.http import JsonResponse
# @login_required(login_url='/user/login')
# @require_http_methods(['GET'])
# def ajax_postcollection(request):
#     res = {'status': 0, 'message': '未知错误'}
#     user=None
#     if request.is_ajax():
#         if not request.user:
#             res = {'status': 401, 'message': '用户未登录'}
#             return JsonResponse(res)
#         else:
#             user = User.objects.get(id = request.user.id)
#         msg = '你的用户名为：' + user.username + '\r\n验证码为：'
#         user.email_user('邮箱重置', msg)  # 发送邮件
#         res['status'] = 200
#         res['message'] = '邮件发送成功'
#         return JsonResponse(res)
#     return JsonResponse(res)