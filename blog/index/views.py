from . import models
from .forms import CommentForm
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from notifications.signals import notify
from django.template import RequestContext
from django.shortcuts import render, redirect
from blog import paginatorPage
from .models import Post, Comment, Like, Dynamic, Collection
from django.views.decorators.http import require_http_methods
from user.models import MyUser as User, Dynamic as UserDynamic, Attention


def get_root():
    return User.objects.filter(is_superuser=1).order_by('id').first()


def get_notifications():
    return User.objects.filter(username='notifications').first()


def get_name(user):
    return str(
        user.get_full_name() if (
            user.get_full_name()) else user.username)


def get_user(request):
    return User.objects.filter(username=request.user.username).first()

# Create your views here.

def defaultView(request):
    return render(request, 'default.html', locals(), RequestContext(request))

def indexView(request):
    '''
    首页
    :param request: 客户端请求头
    :return: html页面
    '''
    page = request.GET.get('page', 1)
    post_list = Post.objects.all().order_by('-time')  # 博客文章列表
    post_read = Post.objects.all().order_by('-readnumber')[:5]  # 博客文章列表
    archive_list = Post.objects.distinct_date()
    comment_list = Comment.objects.all().order_by('-time')[:5]  # 博客评论列表
    for post in post_read:
        if len(post.title) > 12:
            post.title = post.title[:12] + '...'
    paginator, pageInfo = paginatorPage(post_list,settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE,page)  # 文章分页
    return render(request, 'index.html', locals(), RequestContext(request))


def postView(request, id):
    '''
    博客文章
    :param request: 客户端请求头
    :param id: 博客文章id
    :return: html页面
    '''
    post = Post.objects.get(id=id)
    form, page, user = CommentForm(), request.GET.get('page', 1), None
    # 提交评论
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        content = request.POST.get('content', '')
        if content != '' or content is not None:
            comment = Comment(
                content=content,
                post=post,
                user=user,
                time=timezone.now())
            comment.save()
            if get_root() != user:
                notify.send(
                    get_notifications(),
                    recipient=user,
                    verb=get_name(user) +
                    ' 评论了你的文章<br/>',
                    level='info')
            messages.success(request, '评论成功')
        else:
            messages.error(request, '评论失败')
        return redirect(request.get_raw_uri())
    # 动态列表信息
    dynamic = Dynamic.objects.filter(post=id).first()
    userdynamic = UserDynamic.objects.filter(user=post.user).first()
    like_list = Like.objects.filter(post=post)
    collection_list = Collection.objects.filter(post=post)
    attention_list = Attention.objects.filter(attention_id=post.user.id)
    if not userdynamic:  # 如果用户动态列表不存在就创建
        userdynamic = UserDynamic(
            user=post.user,
            dynamic_search=0,
            dynamic_like=0,
            dynamic_attention=0)
        userdynamic.save()
    if not dynamic:  # 如果博客动态列表不存在就创建
        dynamic = Dynamic(
            post=post,
            dynamic_like=0,
            dynamic_collection=0,
            dynamic_search=0)
        dynamic.save()
    num_attention, user_info = userdynamic.dynamic_attention, post.user
    if request.user.id:
        user = get_user(request)
        if post.user.id != request.user.id:
            post.readnumber = int(post.readnumber) + 1
            post.save()
    # 评论分页
    comment = Comment.objects.filter(post=post).order_by('-time').all()
    paginator, pageInfo = paginatorPage(
        comment, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE,page)
    return render(request, 'post.html', locals(), RequestContext(request))

def aboutView(request):
    return render(request, 'about.html', locals(), RequestContext(request))

def archive(request):
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    if year and month:
        article_list = Post.objects.filter(time__icontains=year + '-' + month).order_by('-time').all()
    else:
        article_list = Post.objects.filter().order_by('-time').all()
    # 根据参数year,month进行过滤， 记得字段名+__icontains 表大小写不敏感的包含匹配
    return render(request, 'archive.html', locals())

@require_http_methods(['GET'])
def ajax_postlike(request, id):
    '''
    点赞博客文章
    :param request: 客户端请求头
    :param id: 要点赞文章的id
    :return: json数据
    '''
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=id)
        like = Like.objects.filter(user=user, post=post).first()
        dynamic = Dynamic.objects.filter(post=post).first()
        if not dynamic:
            dynamic = Dynamic(post=post)  # 文章动态信息列表不存在就创建
        if not like:
            like = Like(post=post, user=user, is_like=0)  # 文章点赞列表不存在就创建
        if like.is_like == 1:
            like.is_like = 0
            if int(dynamic.dynamic_like) >= 1:
                dynamic.dynamic_like = int(dynamic.dynamic_like) - 1  # 防止出现负数
            res['status'] = 200
            res['message'] = '取消点赞'
        else:
            like.is_like = 1
            dynamic.dynamic_like = int(dynamic.dynamic_like) + 1
            res['status'] = 200
            res['message'] = '点赞成功'
        if dynamic.save() or like.save():
            res['status'] = 401
            res['message'] = '写入数据库失败'
    return JsonResponse(res)


@require_http_methods(['GET'])
def ajax_postcollection(request, id):
    '''
    收藏博客文章
    :param request: 客户端请求头
    :param id: 要收藏文章的id
    :return: json数据
    '''
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=id)
        collection = Collection.objects.filter(user=user, post=post).first()
        dynamic = Dynamic.objects.filter(post=post).first()
        if not dynamic:
            dynamic = Dynamic(post=post)  # 文章动态信息列表不存在就创建
        if not collection:
            collection = Collection(
                post=post, user=user, is_collection=0)  # 文章收藏列表不存在就创建
        if collection.is_collection == 1:
            collection.is_collection = 0
            if int(dynamic.dynamic_collection) >= 1:
                dynamic.dynamic_collection = int(
                    dynamic.dynamic_collection) - 1  # 防止出现负数
            res['status'] = 200
            res['message'] = '取消收藏'
        else:
            collection.is_collection = 1
            dynamic.dynamic_collection = int(dynamic.dynamic_collection) + 1
            res['status'] = 200
            res['message'] = '收藏成功'
        if dynamic.save() or collection.save():
            res['status'] = 401
            res['message'] = '写入数据库失败'
    return JsonResponse(res)


def guestbookView(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        title = request.POST.get("title")
        content = request.POST.get("content")
        publish = timezone.now()
        message = models.Message(
            title=title,
            content=content,
            username=username,
            publish=publish)
        message.save()
        messages.success(request, '留言成功')
        return redirect('/guestbook/')
    page = request.GET.get('page', 1)
    messageslist = models.Message.objects.all().order_by('-publish')
    paginator, pageInfo = paginatorPage(messageslist,settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE,page)
    return render(request, 'guestbook.html', locals(), RequestContext(request))

def ContributionView(request):
    return render(request, 'QR.html')