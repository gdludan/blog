from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from index.models import Post
from haystack.views import SearchView as Search
from user.models import MyUser,Dynamic as UserDynamic
from index.models import Dynamic as PostDynamic
# 视图以通用视图实现
#站内搜索
class MySearchPostView(Search):# 文章搜索
    # 模版文件
    template = 'search_post.html'
    # 重写响应方式，如果请求参数q为空，返回模型Song的全部数据，否则根据参数q搜索相关数据
    def create_response(self):
        if not self.request.GET.get('q', ''):
            show_all = True
            post = Post.objects.all().order_by('-time')
            paginator = Paginator(post, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            except PageNotAnInteger:
                # 如果参数page的数据类型不是整型，则返回第一页数据
                page = paginator.page(1)
            except EmptyPage:
                # 用户访问的页数大于实际页数，则返回最后一页的数据
                page = paginator.page(paginator.num_pages)
            return render(self.request, self.template, locals())
        else:
            show_all = False
            qs = super(MySearchPostView, self).create_response()
            return qs

class MySearchMyUserView(Search):# 用户搜索
    # 模版文件
    template = 'search_user.html'
    # 重写响应方式，如果请求参数q为空，返回模型Song的全部数据，否则根据参数q搜索相关数据
    def create_response(self):
        if not self.request.GET.get('q', ''):
            show_all = True
            myuser = MyUser.objects.all().order_by('-id')
            paginator = Paginator(myuser, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            except PageNotAnInteger:
                # 如果参数page的数据类型不是整型，则返回第一页数据
                page = paginator.page(1)
            except EmptyPage:
                # 用户访问的页数大于实际页数，则返回最后一页的数据
                page = paginator.page(paginator.num_pages)
            return render(self.request, self.template, locals())
        else:
            show_all = False
            qs = super(MySearchMyUserView, self).create_response()
            return qs