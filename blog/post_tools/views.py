from .forms import *
import datetime,pytz,blog
from index.models import Post
from django.conf import settings
from django.shortcuts import render,redirect
from user.models import MyUser as User,UPfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='/user/login')
def NewVisew(request):
    '''
    新建文章
    :param request: 客户端请求头
    :return: html页面或者跳转到主页
    '''
    form = PostForm()
    title__post ='发布文章'#按钮名称
    if request.method == 'POST':
        user = User.objects.get(id= request.user.id)
        post = Post(title=request.POST.get('title',''),content=request.POST.get('content',''),user=user,time=datetime.datetime.now(tz=pytz.timezone('UTC')))
        post.save()
        return redirect('/user/home')
    return render(request, 'post_file.html', locals())

@login_required(login_url='/user/login')
def EidtorVisew(request,post_id):
    '''
    修改文章
    :param request: 客户端请求头
    :param post_id: 博客文章id
    :return: html页面或者跳转到主页
    '''
    form = PostForm()
    title__post ='确定修改'#按钮名称
    post =Post.objects.get(id = post_id)
    if User.objects.get(id=request.user.id) == post.user:return redirect('/')#判断当前用户是否为此文章作者
    if request.method == 'POST':
        post.title = request.POST.get('title',post.title)
        post.content = request.POST.get('content',post.content)
        post.last_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
        post.save()
        return redirect('/user/home')
    post__title = post.title
    post__content = post.content
    return render(request, 'post_file.html', locals())

@login_required(login_url='/user/login')
def UploadFileView(request):
    '''
    上传文件
    :param request: 客户端请求头
    :return: html页面
    '''
    user = User.objects.get(id=request.user.id)
    if user.is_upload == 0 : return redirect('/')#检测用户上传权限
    form = UPfileForm()
    page = request.GET.get('page',1)
    if request.method == 'POST':
        file = request.FILES['file']
        name,filename= blog.randNmae() + '_' + file.name, file.name
        Upload_file,user = settings.MEDIA_ROOT_FILE+name,User.objects.get(id = request.user.id)
        with open(Upload_file,'wb') as f:
            for file_bytes in file.chunks():
                f.write(file_bytes)
        import platform
        if platform.system() !='Windows':str='stat'#UNIX和类UNIX(例如linux)系统会少四个字符
        else:str =''
        upfile=UPfile(name=filename,file='/'+str+Upload_file.lstrip(settings.BASE_DIR) ,
                      user=user,time=datetime.datetime.now(tz=pytz.timezone('UTC')))
        upfile.save()
        tips= '上传文件成功'
    upfile = UPfile.objects.filter(user=user).order_by('-time').all()
    post_num = len(upfile)
    paginator = Paginator(upfile, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'UploadFile.html', locals())