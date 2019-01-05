from django.urls import path
from . import views
# 设置首页的URL地址信息
urlpatterns = [
    path('post_new',views.NewVisew,name='new'),# 新建文章
    path('post_eidtor/<int:post_id>',views.EidtorVisew,name='eidtor'),#编辑文章
    path('UploadFile',views.UploadFileView,name='Upload_file'),#上传文件
]
