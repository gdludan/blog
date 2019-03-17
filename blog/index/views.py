import pytz,datetime
from .forms import CommentForm
from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Post,Comment,Like,Dynamic,Collection
from django.views.decorators.http import require_http_methods
from user.models import MyUser as User,Dynamic as UserDynamic,Attention
from blog import paginatorPage,timeago_or_time
from notifications.signals import notify

def get_root():
    return User.objects.filter(is_superuser=1).order_by('id').first()

def get_name(user):
    return str(user.get_full_name() if (user.get_full_name()) else user.username)

def get_user(request):
    return User.objects.filter(username=request.user.username).first()

# Create your views here.
def indexView(request):
    '''
    首页
    :param request: 客户端请求头
    :return: html页面
    '''
    page = request.GET.get('page', 1)
    temp,post_list2=None,[]
    post_list = Post.objects.all().order_by('-id')#博客文章列表
    post_read = Post.objects.all().order_by('-readnumber')[:5]#博客文章列表
    comment_list = Comment.objects.all().order_by('-time')[:5]#博客评论列表
    for post in post_read:
        if len(post.title)>12:
            post.title = post.title[:12] + '...'
    for post in post_list:
        post.time =timeago_or_time(post.time)
        if post.date !=temp:
            post_list2.append(post)
            temp=post.date
        if len(post_list2) >= 5:
            break
    paginator,pageInfo= paginatorPage(post_list,15)#文章分页
    # return render(request, 'index.html', locals())
    return render(request, 'index.html', locals(),RequestContext(request))

def postView(request,id):
    '''
    博客文章
    :param request: 客户端请求头
    :param id: 博客文章id
    :return: html页面
    '''
    post = Post.objects.get(id = id)
    form,page,user = CommentForm(),request.GET.get('page', 1),None
    # 提交评论
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        content = request.POST.get('content', '')
        if content!='' or content !=None :
            comment = Comment(content=content,post=post,user=user,
                              time=datetime.datetime.now(tz=pytz.timezone('UTC')))
            comment.save()
            if get_root()!=user:
                notify.send(get_root(), recipient=user,
                            verb= get_name(user) + ' 评论了你的文章<br/>', level='info')
        return redirect(request.get_raw_uri())
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
    num_attention,user_info = userdynamic.dynamic_attention,post.user
    if request.user.id:
        user = get_user(request)
        for i in like_list:
            if i.user.id == user.id and i.is_like== 1: like = 1
        for j in collection_list:
            if j.user.id == user.id and j.is_collection==1 : collection = 1
        for k in attention_list:
            if k.user.id == user.id and k.is_attention ==1 : attention = 1
        post.readnumber = str(int(post.readnumber)+0 if post.user == user else 1);post.save()
    else:
        like,collection,attention = 0,0,0
    #评论分页
    comment = Comment.objects.filter(post=post).order_by('-time').all()
    paginator, pageInfo = paginatorPage(comment, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    post.time = timeago_or_time(post.time)
    for comm in comment:
        comm.time=timeago_or_time(comm.time)
    return render(request, 'post.html',locals(),RequestContext(request))

def aboutView(request):
    return render(request,'about.html',locals(),RequestContext(request))

def Getdate(request,year,month,day):
    if month > 12 or day>31:return HttpResponse('日期错误')
    elif month==2 and day>29:return HttpResponse('日期错误')
    elif month in [4,6,9,11] and day>30:return HttpResponse('日期错误')
    return HttpResponse('{}年{}月{}日'.format(year,month,day))

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

