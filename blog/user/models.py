from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class MyUser(AbstractUser):
    avatar = models.CharField('头像', max_length=255, unique=False,default='/static/images/default.jpg',blank = True)
    mobile = models.CharField('手机号码', max_length=11, unique=False,blank = True,default='')
    is_upload = models.NullBooleanField('是否允许上传文件',blank=True,default=0)
    is_Auxiliary = models.NullBooleanField('辅助管理员',blank=True,default=0)
    ip = models.GenericIPAddressField('上次登录ip地址',default='0.0.0.0')
    ipaddress =  models.CharField('ip物理地址', max_length=128,blank = True,default='')
    def __str__(self):
        return self.username
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '用户信息列表'
        verbose_name_plural = '用户信息列表'

class Profile(models.Model):
    id = models.AutoField('序号', primary_key=True)
    interest = models.CharField('兴趣', max_length=255,blank = True,default='无')
    aims = models.CharField('最近目标', max_length=255,blank = True,default='无')
    motto = models.CharField('座右铭', max_length=255,blank = True,default='无')
    self_reprot = models.CharField('自我介绍', max_length=1024,blank = True,default='这个人很懒，什么也没有写！')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.user.username
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '个人信息列表'
        verbose_name_plural = '个人信息列表'

class UPfile(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('文件名',max_length=256,unique=False,default='')
    file = models.CharField('文件路径',max_length=512,blank=True,default='')
    time = models.DateTimeField('时间', max_length=128, auto_now_add=timezone.now)
    Prohibited =  models.NullBooleanField('文件是否已删除',blank=False,default=0)
    Prohibited_info =  models.CharField('删除信息',blank=False,default='',max_length=256)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.user.username
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '文件信息列表'
        verbose_name_plural = '文件信息列表'

class Attention(models.Model):
    id = models.AutoField('序号', primary_key=True)
    attention_id = models.IntegerField('关注的用户',blank=False,default=0)
    is_attention = models.IntegerField('是否已关注',blank=False,default=0)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return str(self.attention_id)
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '关注信息列表'
        verbose_name_plural = '关注信息列表'

class Dynamic(models.Model):
    id =models.AutoField('序号', primary_key=True)
    dynamic_like = models.IntegerField('点赞次数',blank=True,default=0)
    dynamic_attention = models.IntegerField('关注次数',blank=True,default=0)
    dynamic_search = models.IntegerField('搜索次数',blank=True,default=0)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return str(self.id)
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '用户动态列表'
        verbose_name_plural = '用户动态列表'