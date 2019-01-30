from .models import Message,Type
import xadmin

#数据库表单模型
class MessageAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'content', 'time','ip','type','user','view']
    #过滤器
    list_filter = ['time','ip','type','user','view']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'content', 'time','ip','type','user','view']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

class TypeAdmin(object):
    #图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'type_name']
    #过滤器
    list_filter = ['id', 'type_name']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'type_name']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Type, TypeAdmin)