from django.contrib import admin
from .models import Access, SetCtarl


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'date', 'num']
    # 过滤器
    list_filter = ['id', 'date', 'num']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'date', 'num']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(SetCtarl)
class SetCtarlAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'name', 'is_start']
    # 过滤器
    list_filter = ['id', 'name', 'is_start']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'name', 'is_start']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面
