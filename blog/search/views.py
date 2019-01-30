from index.models import Post
from django.conf import settings
from django.shortcuts import render
from haystack.views import SearchView as Search
#from index.models import Dynamic as PostDynamic
from user.models import MyUser,Dynamic as UserDynamic
from blog import paginatorPage
from django.template import RequestContext
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
            paginator, pageInfo = paginatorPage(post, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            return render(self.request, self.template, locals(),RequestContext(self.request))
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
            paginator, pageInfo = paginatorPage(myuser, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            return render(self.request, self.template, locals(),RequestContext(self.request))
        else:
            show_all = False
            qs = super(MySearchMyUserView, self).create_response()
            return qs