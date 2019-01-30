from django.contrib import admin
from .models import Post,Comment,Dynamic,Like,Collection
from django.conf import settings
# 修改title和header
admin.site.site_title = '卤蛋博客后台管理系统'
admin.site.site_header = '卤蛋博客'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    # list_display = ['id', 'title', 'content', 'time']
    list_display = ['id', 'title', 'time','user','Prohibited','Prohibited_info']
    #过滤器
    list_filter = ['time','user','Prohibited']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    # search_fields = ['title', 'content', 'time']
    search_fields = ['title', 'time','user','Prohibited','Prohibited_info']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面
    # # 修改保存方法
    def save_model(self, request, obj, form, change):
        if change:
            # 获取当前用户名
            user = request.user
            # 使用模型获取修改数据
            title = self.model.objects.get(pk=obj.pk).title
            # 使用表单获取修改数据
            content = form.cleaned_data['content']
            # 写入日志文件
            f = open(settings.BASE_DIR+'//LDblog.log', 'a')
            f.write('产品：' + str(title) + '，被用户：' + str(user) + '修改' + '文章内容\r\n')
            f.close()
        # 使用super可使自定义save_model既保留父类的已有的功能并添加自定义功能。
        super(PostAdmin, self).save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'content', 'time','Prohibited','Prohibited_info']
    #过滤器
    list_filter = ['time','post','Prohibited']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'content', 'time','Prohibited','Prohibited_info']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id','dynamic_like', 'dynamic_collection', 'dynamic_search','post']
    #过滤器
    list_filter = ['dynamic_like', 'dynamic_collection', 'dynamic_search','post']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['dynamic_like',  'dynamic_collection', 'dynamic_search','post']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_like', 'post', 'user']
    #过滤器
    list_filter = [ 'is_like', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'is_like', 'post', 'user']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['id', 'is_collection', 'post', 'user']
    #过滤器
    list_filter = [ 'is_collection', 'post', 'user']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = [ 'is_collection', 'post', 'user']
    # 设置排序方式
    ordering = ['-id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面