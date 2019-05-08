from django.contrib import admin
from .models import Profile
from .models import MyUser, UPfile, Attention, Dynamic, Valid
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'mobile']
    # 在用户信息修改界面添加'mobile','qq','weChat'的信息输入框
    # 将源码的UserAdmin.fieldsets转换成列表格式
    fieldsets = list(UserAdmin.fieldsets)
    # 重写UserAdmin的fieldsets，添加'mobile'的信息录入
    fieldsets[1] = (
        _('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'mobile')})


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'interest', 'aims', 'motto', 'self_reprot']
    # 过滤器
    list_filter = ['user', 'self_reprot']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['interest', 'aims', 'motto']
    # 设置排序方式
    ordering = ['id']


@admin.register(UPfile)
class UPfileAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'file', 'time', 'Prohibited', 'Prohibited_info']
    # 过滤器
    list_filter = ['file', 'time', 'Prohibited']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['file', 'time', 'Prohibited', 'Prohibited_info']
    # 设置排序方式
    ordering = ['id']


@admin.register(Attention)
class AttentionAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'attention_id', 'user']
    # 过滤器
    list_filter = ['attention_id', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['attention_id', 'user']
    # 设置排序方式
    ordering = ['id']


@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'dynamic_like', 'dynamic_attention', 'user']
    # 过滤器
    list_filter = ['dynamic_like', 'dynamic_attention', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['dynamic_like', 'dynamic_attention', 'user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Valid)
class ValidAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'value', 'user', 'is_valid']
    # 过滤器
    list_filter = ['value', 'user', 'is_valid']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['value', 'user', 'is_valid']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面
