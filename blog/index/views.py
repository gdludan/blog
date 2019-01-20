import pytz,datetime
from .forms import CommentForm
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Post,Comment,Like,Dynamic,Collection
from django.views.decorators.http import require_http_methods
from user.models import MyUser as User,Dynamic as UserDynamic,Attention
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def indexView(request):
    '''
    首页
    :param request: 客户端请求头
    :return: html页面
    '''
    Open_source = True
    page = request.GET.get('page', 1)
    title = "首页"
    post_list = Post.objects.all().order_by('-id')#博客文章列表
    paginator = Paginator(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)#文章分页
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())

def postView(request,id):
    '''
    博客文章
    :param request: 客户端请求头
    :param id: 博客文章id
    :return: html页面
    '''
    post = Post.objects.get(id = id)
    # 提交评论
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        content = request.POST.get('content', '')
        if content!='' or content !=None :
            comment = Comment(content=content,post=post,user=user,
                              time=datetime.datetime.now(tz=pytz.timezone('UTC')))
            comment.save()
        return redirect(request.get_raw_uri())
    form,page,user = CommentForm(),request.GET.get('page', 1),None
    title,user_info = post.title,post.user
    # 动态列表信息
    dynamic= Dynamic.objects.filter(post=id).first()
    userdynamic =UserDynamic.objects.filter(user=post.user).first()
    like_list = Like.objects.filter(post=post)
    collection_list = Collection.objects.filter(post=post)
    attention_list = Attention.objects.filter(attention_id=post.user.id)
    if not userdynamic:#如果用户动态列表不存在就创建
        userdynamic=UserDynamic(user=post.user,dynamic_search=0,dynamic_like=0,dynamic_attention=0)
        userdynamic.save()
    if not dynamic:#如果博客动态列表不存在就创建
        dynamic = Dynamic(post=post,dynamic_like=0,dynamic_collection=0,dynamic_search=0)
        dynamic.save()
    num_like, num_collection,num_attention = dynamic.dynamic_like,dynamic.dynamic_collection,userdynamic.dynamic_attention
    if request.user.id:
        is_login = True;post.readnumber = str(int(post.readnumber)+1);post.save()
        user = User.objects.get(id = request.user.id)
        for i in like_list:
            if i.user.id == user.id and i.is_like== 1: like = 1
        for j in collection_list:
            if j.user.id == user.id and j.is_collection==1 : collection = 1
        for k in attention_list:
            if k.user.id == user.id and k.is_attention ==1 : attention = 1
    else:
        like, is_login, collection,attention = 0, False, 0,0
    #评论分页
    comment = Comment.objects.filter(post=post).all().order_by('-time')
    number = len(comment)
    paginator = Paginator(comment, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'post.html',locals())

@require_http_methods(['GET'])
def ajax_postlike(request,id):
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
        user = User.objects.get(id = request.user.id)
        post = Post.objects.get(id=id)
        like = Like.objects.filter(user=user,post=post).first()
        dynamic= Dynamic.objects.filter(post=post).first()
        if not dynamic:dynamic = Dynamic(post=post)#文章动态信息列表不存在就创建
        if not like:like = Like(post=post,user=user,is_like=0)#文章点赞列表不存在就创建
        if like.is_like == 1:
            like.is_like= 0
            if int(dynamic.dynamic_like)>=1:dynamic.dynamic_like = int(dynamic.dynamic_like)-1#防止出现负数
            res['status']=200
            res['message']='取消点赞'
        else:
            like.is_like = 1
            dynamic.dynamic_like = int(dynamic.dynamic_like)+1
            res['status']=200
            res['message']='点赞成功'
        if dynamic.save() or like.save():
            res['status'] = 401
            res['message'] = '写入数据库失败'
    return JsonResponse(res)

@require_http_methods(['GET'])
def ajax_postcollection(request,id):
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
        user = User.objects.get(id = request.user.id)
        post = Post.objects.get(id=id)
        collection = Collection.objects.filter(user=user,post=post).first()
        dynamic= Dynamic.objects.filter(post=post).first()
        if not dynamic:dynamic = Dynamic(post=post)#文章动态信息列表不存在就创建
        if not collection:collection = Collection(post=post,user=user,is_collection=0)#文章收藏列表不存在就创建
        if collection.is_collection == 1:
            collection.is_collection = 0
            if int(dynamic.dynamic_collection)>=1:dynamic.dynamic_collection = int(dynamic.dynamic_collection)-1#防止出现负数
            res['status'] = 200
            res['message'] = '取消收藏'
        else:
            collection.is_collection = 1
            dynamic.dynamic_collection = int(dynamic.dynamic_collection)+1
            res['status'] = 200
            res['message'] = '收藏成功'
        if dynamic.save() or collection.save():
            res['status'] = 401
            res['message'] = '写入数据库失败'
    return JsonResponse(res)
