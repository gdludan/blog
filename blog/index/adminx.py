import xadmin
from xadmin.views import CommAdminView
from xadmin import views
from .models import Post,Comment,Dynamic,Like,Collection

#数据库表单模型
class PostAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    # list_display = ['id', 'title', 'content', 'time']
    list_display = ['id', 'title', 'time','user','Prohibited','Prohibited_info']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    # search_fields = ['title', 'content', 'time']
    search_fields = ['title', 'time','user','Prohibited','Prohibited_info']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class CommentAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'content', 'time','Prohibited','Prohibited_info']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'content', 'time' ,'Prohibited','Prohibited_info']
    #list_filter = ['label_id','label_name']  # 筛选
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class DynamicAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id','dynamic_like', 'dynamic_collection', 'dynamic_search','post']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['dynamic_like',  'dynamic_collection', 'dynamic_search','post']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class LikeAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_like', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'is_like', 'post', 'user']
    # 设置排序方式
    ordering = ['id']

class CollectionAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_collection', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'is_collection', 'post', 'user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Dynamic, DynamicAdmin)
xadmin.site.register(Like, LikeAdmin)
xadmin.site.register(Collection, CollectionAdmin)

class BaseSetting(object):
    #设置主题功能
    enable_themes = True
    use_bootswatch = True

class CustomAdmin(object):
    site_title='卤蛋博客后台管理'
    site_footer='卤蛋版权所有'
    #设置伸缩
    #menu_style='accordion'

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(CommAdminView,CustomAdmin)