from django.urls import path
from . import views
# 设置首页的URL地址信息
urlpatterns = [
    path('post', views.MySearchPostView(), name='haystack_post'),#搜索文章
    path('user', views.MySearchMyUserView(), name='haystack_user'),#搜索用户
]
