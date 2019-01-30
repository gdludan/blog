from . import views
from django.urls import path
# 设置首页的URL地址信息
urlpatterns = [
    path('',views.messageIndexVisw, name='message'),#显示消息
    path('set/<int:user>',views.set, name='setmessage'),#设置
    # path('unread/<int:user>',views.unread, name='unreadmessage'),#获取没有读取消息
    path('setread/<int:user>',views.setread, name='setread'),#设置用户消息为已读取
    path('setmess',views.setmess, name='setmess'),
    path('delread/<int:user>',views.delread, name='delread'),
    path('num',views.num, name='nummessage'),
]

