import xadmin

from .models import Profile,UPfile,Attention,Dynamic

#数据库表单模型

class ProfileAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'interest', 'aims', 'motto','self_reprot']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'interest', 'aims', 'motto']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class UPfileAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'file','time','Prohibited','Prohibited_info']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'file','time','Prohibited','Prohibited_info']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class AttentionAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'attention_id','user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'attention_id','user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class DynamicAdmin(object):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id','dynamic_like', 'dynamic_attention', 'dynamic_search','user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['dynamic_like', 'dynamic_attention', 'dynamic_search','user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

xadmin.site.register(UPfile, UPfileAdmin)
xadmin.site.register(Profile, ProfileAdmin)
xadmin.site.register(Attention, AttentionAdmin)
xadmin.site.register(Dynamic, DynamicAdmin)