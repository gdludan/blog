import xadmin
from .models import Access

#数据库表单模型
class AccessAdmin(object):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'date', 'num']
    #过滤器
    list_filter = ['id', 'date', 'num']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'date', 'num']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

xadmin.site.register(Access, AccessAdmin)