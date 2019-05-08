from django.contrib import admin
from .models import Post, Comment, Dynamic, Like, Collection, Message, Tags, Reply

# 修改title和header
admin.site.site_title = '卤蛋博客后台管理系统'
admin.site.site_header = '卤蛋博客'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    # list_display = ['id', 'title', 'content', 'time']
    list_display = [
        'id',
        'title',
        'time',
        'user',
        'type',
        'Prohibited',
        'Prohibited_info']
    # 过滤器
    list_filter = ['time', 'user', 'Prohibited', 'type']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    # search_fields = ['title', 'content', 'time']
    search_fields = [
        'title',
        'time',
        'user',
        'type',
        'Prohibited',
        'Prohibited_info']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'name', 'post']
    # 过滤器
    list_filter = ['name', 'post']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['name', 'post']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'content', 'time', 'Prohibited', 'Prohibited_info', 'post']
    # 过滤器
    list_filter = ['time', 'post', 'Prohibited']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['content', 'time', 'Prohibited', 'Prohibited_info', 'post']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'content', 'time', 'Prohibited', 'Prohibited_info', "comment"]
    # 过滤器
    list_filter = ['time', 'comment', 'Prohibited']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['content', 'time', 'Prohibited', 'Prohibited_info', "comment"]
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'dynamic_like', 'dynamic_collection', 'post']
    # 过滤器
    list_filter = ['dynamic_like', 'dynamic_collection', 'post']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['dynamic_like', 'dynamic_collection', 'post']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_like', 'post', 'user']
    # 过滤器
    list_filter = ['is_like', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['is_like', 'post', 'user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_collection', 'post', 'user']
    # 过滤器
    list_filter = ['is_collection', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['is_collection', 'post', 'user']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'username', 'publish']
    # 过滤器
    list_filter = ['id', 'username', 'publish']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'username', 'publish']
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面
