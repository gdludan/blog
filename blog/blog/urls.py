"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),# django原生后台
    path('xadmin/', xadmin.site.urls,name='xadmin'),# xadmin后台
    path('', include('index.urls')),# 网站首页
    path('fun/', include('fun.urls')),# 游戏和一些小玩意
    path('user/', include('user.urls')),# 用户中心及其他用户操作
    path('search/', include('search.urls')),# 站内搜索
    path('config/', include('set_config.urls')),# 用户配置
    path('tools/', include('post_tools.urls')),# 网站工具
    path('captcha/', include('captcha.urls')),# 验证码接口
    path('message/', include('message.urls')),# 消息
    path('tinymce/', include('tinymce.urls')), # 固定写法，其实是映射到人家写好的应用
]
