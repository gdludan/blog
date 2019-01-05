from django.shortcuts import render,redirect
from .models import Post,Comment,Like,Dynamic,Collection
from .forms import CommentForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pytz,datetime
from user.models import MyUser as User,Dynamic as UserDynamic,Attention
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from captcha.models import CaptchaStore
from django.views.decorators.http import require_http_methods

# Create your views here.
def indexView(request):
    Open_source = True
    page = request.GET.get('page', 1)
    title = "首页"
    post_list = Post.objects.all().order_by('-time')
    paginator = Paginator(post_list, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())

def postView(request,id):
    #title = "文章"
    form = CommentForm()
    post = Post.objects.get(id = id)
    post.readnumber = str(int(post.readnumber)+1)
    post.save()
    title = post.title
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if request.POST.get('content', ''):
            content = request.POST.get('content', '')
            comment = Comment(content=content,post=post,user=user,
                              time=datetime.datetime.now(tz=pytz.timezone('UTC')))
            comment.save()
        return redirect(request.get_raw_uri())
    dynamic= Dynamic.objects.filter(post=id).first()
    userdynamic =UserDynamic.objects.filter(user=post.user).first()
    like_list = Like.objects.filter(post=post)
    collection_list = Collection.objects.filter(post=post)
    attention_list = Attention.objects.filter(attention_id=post.user.id)
    if not userdynamic:
        userdynamic=UserDynamic(user=post.user,dynamic_search=0,dynamic_like=0,dynamic_attention=0)
        userdynamic.save()
    num_attention= userdynamic.dynamic_attention
    if not dynamic:
        dynamic = Dynamic(post=post,dynamic_like=0,dynamic_collection=0,dynamic_search=0)
        dynamic.save()
    num_like, num_collection = dynamic.dynamic_like,dynamic.dynamic_collection
    user_info = post.user
    if request.user.id:
        is_login = True
        user = User.objects.get(id = request.user.id)
        for i in like_list:
            if i.user.id == user.id and i.is_like== 1: like = 1
        for j in collection_list:
            if j.user.id == user.id and j.is_collection==1 : collection = 1
        for k in attention_list:
            if k.user.id == user.id and k.is_attention ==1 : attention = 1
    else:
        like, is_login, collection,attention = 0, False, 0,0
        user = None
    #评论页数
    page = request.GET.get('page', 1)
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
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id = request.user.id)
        post = Post.objects.get(id=id)
        like = Like.objects.filter(user=user,post=post).first()
        dynamic= Dynamic.objects.filter(post=post).first()
        if not like:
            like = Like(post=post,user=user,is_like=0)
        if like.is_like == 1:
            like.is_like= 0
            if int(dynamic.dynamic_like)>=1:
                dynamic.dynamic_like = int(dynamic.dynamic_like)-1
            res['status']=200
            res['message']='取消点赞'
        else:
            like.is_like = 1
            dynamic.dynamic_like = int(dynamic.dynamic_like)+1
            res['status']=200
            res['message']='点赞成功'
        dynamic.save()
        like.save()
        return JsonResponse(res)
    return JsonResponse(res)

@require_http_methods(['GET'])
def ajax_postcollection(request,id):
    res = {'status': 0, 'message': '未知错误'}
    if request.is_ajax():
        if not request.user:
            res = {'status': 401, 'message': '用户未登录'}
            return JsonResponse(res)
        user = User.objects.get(id = request.user.id)
        post = Post.objects.get(id=id)
        collection = Collection.objects.filter(user=user,post=post).first()
        dynamic= Dynamic.objects.filter(post=post).first()
        if not collection:
            collection = Collection(post=post,user=user,is_collection=0)
        if collection.is_collection == 1:
            collection.is_collection = 0
            if int(dynamic.dynamic_collection)>=1:
                dynamic.dynamic_collection = int(dynamic.dynamic_collection)-1
            res['status'] = 200
            res['message'] = '取消收藏'
        else:
            collection.is_collection = 1
            dynamic.dynamic_collection = int(dynamic.dynamic_collection)+1
            res['status'] = 200
            res['message'] = '收藏成功'
        collection.save()
        dynamic.save()
        return JsonResponse(res)
    return JsonResponse(res)
