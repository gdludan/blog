from django.conf import settings
from django.conf.urls import static
import notifications.urls
from xadmin.plugins import xversion
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
from django.urls import path, include

import xadmin
xadmin.autodiscover()
xversion.register_models()
urlpatterns = [
    path('admin/', admin.site.urls),  # django原生后台
    path('xadmin/', xadmin.site.urls),  # xadmin后台
    path('', include('index.urls')),  # 网站首页
    path('api/', include('api.urls')),  # api接口
    path('fun/', include('fun.urls')),  # 一些小玩意
    path('user/', include('user.urls')),  # 用户中心及其他用户操作
    path('search/', include('search.urls')),  # 站内搜索
    path('config/', include('set_config.urls')),  # 用户配置
    path('tools/', include('tools.urls')),  # 网站工具
    path('captcha/', include('captcha.urls')),  # 验证码接口
    path('tinymce/', include('tinymce.urls')),  # 固定写法，其实是映射到人家写好的应用
    path(
        'notifications/',
        include(
            notifications.urls,
            namespace='notifications')),
]
urlpatterns += static.static(settings.STATIC_URL,
                             document_root=settings.STATIC_ROOT)
