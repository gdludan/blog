''' Django notifications admin file '''
# -*- coding: utf-8 -*-
import xadmin
from .models import Notification


class NotificationAdmin(object):
    # 图标
    #model_icon = 'fa fa-picture-o'
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = [
        'recipient',
        'actor',
        'level',
        'target',
        'unread',
        'public']
    # 过滤器
    list_filter = ['level', 'unread', 'public', 'timestamp', ]
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['level', 'unread', 'public', 'timestamp', ]
    # 设置排序方式
    ordering = ['id']
    refresh_times = [5, 2]  # 自动刷新后台管理页面
    # raw_id_fields = ['recipient',]

# 暂时关闭xadmin的Notification 数据模型，
# AttributeError at /xadmin/notifications/notification/
# 'GenericForeignKey' object has no attribute 'flatchoices'
#xadmin.site.register(Notification, NotificationAdmin)
