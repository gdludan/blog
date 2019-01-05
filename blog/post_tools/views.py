from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from user.models import MyUser,UPfile
from index.models import *
import datetime,pytz,blog
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='/user/login')
def NewVisew(request):
    form = PostForm()
    title__post ='发布文章'
    if request.method == 'POST':
        form =PostForm(request.POST)
        user = MyUser.objects.get(id= request.user.id)
        post = Post(title=request.POST.get('title',''),content=request.POST.get('content',''),user=user,time=datetime.datetime.now(tz=pytz.timezone('UTC')))
        post.save()
        return redirect('/user/home')
    return render(request, 'post_file.html', locals())

@login_required(login_url='/user/login')
def EidtorVisew(request,post_id):
    form = PostForm()
    title__post ='确定修改'
    post =Post.objects.get(id = post_id)
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if user == post.user or user.is_superuser:
            post.title = request.POST.get('title',post.title)
            post.content = request.POST.get('content',post.content)
            post.last_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
            post.save()
            return redirect('/user/home')
        else:
            tips = '你不是'+post.title+'的作者或管理员，不能更改此文章任何内容!'
    post__title = post.title
    post__content = post.content
    return render(request, 'post_file.html', locals())

@login_required(login_url='/user/login')
def UploadFileView(request):
    user = User.objects.get(id=request.user.id)
    if user.is_upload ==0:
        return redirect('/')
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
        str =''
        if platform.system() !='Windows':
            str='stat'
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