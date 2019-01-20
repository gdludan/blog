from . import views
from django.urls import path
# 设置首页的URL地址信息
urlpatterns = [
    path('login', views.loginView, name='login'),# 登录
    path('regist', views.registView, name='regist'),# 注册
    path('home', views.homeView, name='home'),# 用户中心
    path('info/<str:username>', views.userView, name='user'),# 用户信息
    path('logout', views.logoutView, name='logout'),# 注销登录
    path('passwd', views.passwdView, name='password'),# 密码重置
    path('findPassword', views.findPassword, name='findPassword'),#找回密码
    path('attention/<int:id>', views.ajax_userattention, name='post_collection'),#用户关注
    path('ajax_val', views.ajax_val, name='ajax_val'),# 验证码验证ajax接口
]
