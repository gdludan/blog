from django.conf import settings
from django.shortcuts import render, redirect
from haystack.views import SearchView as Search
from index.models import Post
from user.models import MyUser as User
from blog import paginatorPage
from django.template import RequestContext
from django.db.models import Q


class MySearchPostView(Search):  # 文章搜索
    # 模版文件
    template = 'search_post.html'
    # 重写响应方式，如果请求参数q为空，返回模型Song的全部数据，否则根据参数q搜索相关数据

    def create_response(self):
        page = self.request.GET.get('page', 1)
        if not self.request.GET.get('q', ''):
            post = []
            paginator, page = paginatorPage(
                post, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE, page)
            return render(
                self.request,
                self.template,
                locals(),
                RequestContext(
                    self.request))
        else:
            qs = super(MySearchPostView, self).create_response()
            return qs


def searchView(request):
    page = request.GET.get('page', 1)
    query = request.GET.get('q', '').strip()
    # 分词：按空格 & | ~
    search = Q(
        id__icontains=query) | Q(
        id__icontains=query) | Q(
            username__icontains=query)
    search = search | Q(
        username__icontains=query) | Q(
        first_name__icontains=query)
    search = search | Q(
        last_name__icontains=query) | Q(
        last_name__icontains=query)
    search = search | Q(first_name__icontains=query)
    search_users = User.objects.filter(search).all()

    paginator, page = paginatorPage(
        search_users, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE, page)  # 文章分页
    return render(request, 'search_user.html', locals())
