import requests
from . import views
from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls import url
from django.shortcuts import redirect
# 设置首页的URL地址信息
robots = 'User-agent: *\nDisallow: /admin/\nDisallow: /xadmin/\n'
urlpatterns = [
    path('default.html', views.defaultView, name='default'),  # 展示页面
    path('index.html', views.indexView, name='indexHtml'),  # 首页
    path('', views.indexView, name='index'),  # 首页
    path('post/', include([
        path('<int:id>', views.postView, name='post'),  # 博客文章
        path('comment/<int:id>', views.reply, name='comment_reply'),  #
        path('like/<int:id>', views.ajax_postlike, name='post_like'),  # 点赞博客文章
        path(
            'collection/<int:id>',
            views.ajax_postcollection,
            name='post_collection'),
        # 收藏博客文章
    ])),  # 二级路由
    path('about', views.aboutView, name='about'),  # 关于
    url(r'^archive/$', views.archive, name='archive'),  # 归档
    path('guestbook/', views.guestbookView, name='guestbook'),  # 留言墙主页
    path('contribution', views.ContributionView, name='Contribution'),  # 留言墙主页
    path('Visitor', views.WebsiteVisitorVolumeView, name='Visitor'),  # 访问量视图
]
urlpatterns += [
    # 使用github 生成的默认头像，减少 nginx 压力
    path("static/images/default.jpg", lambda r:HttpResponse(
        requests.get("https://github.com/identicons/guest.png").content, content_type='image/png')),
    path('robots.txt', lambda r: HttpResponse(
        robots, content_type='text/plain')),
    path('favicon.ico', lambda r:redirect(
        '/static/favicon.ico')),  # 兼容国内浏览器ico图标方式1
    # path('favicon.ico',lambda r:HttpResponse(open(settings.BASE_DIR+'\\static\\favicon.ico','rb').read(),
    #                                          content_type='image/ico',)),#兼容国内浏览器ico图标方式2
]
