from . import views
from django.urls import path
# 设置首页的URL地址信息
urlpatterns = [
    path('edit_gravatar',views.edit_gravatarView,name='edit_gravatar'),#更改头像
    path('edit_profile',views.edit_profileView,name='edit_profile'),#修改个人信息
    path('collection_management',views.collection_managementView,name='collection_management'),#收藏文章管理
    path('attention_management',views.attention_managementView,name='attention_management'),#关注博主管理
]
