from . import views
from django.urls import path,include
# 设置首页的URL地址信息
urlpatterns = [
    path('', views.indexView, name='index'),#首页
    path('post/',include([
        path('<int:id>', views.postView, name='post'),#博客文章
        path('like/<int:id>', views.ajax_postlike, name='post_like'),#点赞博客文章
        path('collection/<int:id>', views.ajax_postcollection, name='post_collection'),# 收藏博客文章
    ])),#二级路由系统
]
