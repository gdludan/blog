from django.db import models
from user.models import MyUser as User
from django.utils import timezone
from tinymce.models import HTMLField
# Create your models here.

class Post(models.Model):
    id = models.AutoField('序号', primary_key=True)
    title = models.CharField('标题', max_length=255,default='')
    content = HTMLField('内容',default='')
    date = models.DateField('文章创建日期',max_length=125,auto_now_add=timezone.now)
    time = models.DateTimeField ('文章创建时间', max_length=125,auto_now_add=timezone.now)
    readnumber = models.IntegerField('文章阅读数量',default=0)
    Prohibited =  models.NullBooleanField('文章是否禁止查看',blank=False,default=0)
    Prohibited_info =  models.CharField('禁止信息',blank=False,default='违规',max_length=256)
    last_time = models.DateTimeField ('最后修改时间', max_length=125,auto_now_add=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.title
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客文章列表'
        verbose_name_plural = '博客文章列表'

class Comment(models.Model):
    id = models.AutoField('序号', primary_key=True)
    content = HTMLField('内容')
    time = models.DateTimeField ('时间', max_length=128,auto_now_add=timezone.now)
    Prohibited =  models.NullBooleanField('评论是否禁止查看',blank=False,default=0)
    Prohibited_info =  models.CharField('禁止信息',blank=False,default='违规',max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.content
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客评论列表'
        verbose_name_plural = '博客评论列表'

class SonComment(models.Model):
    id = models.AutoField('序号', primary_key=True)
    content = HTMLField('内容')
    time = models.DateTimeField ('时间', max_length=128,auto_now_add=timezone.now)
    Prohibited =  models.NullBooleanField('评论是否禁止查看',blank=False,default=0)
    Prohibited_info =  models.CharField('禁止信息',blank=False,default='违规',max_length=256)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,verbose_name='评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return self.content
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客子评论列表'
        verbose_name_plural = '博客子评论列表'

class Dynamic(models.Model):
    id =models.AutoField('序号', primary_key=True)
    dynamic_like = models.IntegerField('点赞次数',blank=True,default=0)
    dynamic_collection = models.IntegerField('收藏次数',blank=True,default=0)
    dynamic_search = models.IntegerField('搜索次数',blank=True,default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='文章')
    def __str__(self):
        return self.post.title
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客动态列表'
        verbose_name_plural = '博客动态列表'

class Like(models.Model):
    id = models.AutoField('序号', primary_key=True)
    is_like =models.NullBooleanField('点赞状态',blank=False,default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return str(self.id)
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客点赞列表'
        verbose_name_plural = '博客点赞列表'

class Collection(models.Model):
    id = models.AutoField('序号', primary_key=True)
    is_collection = models.NullBooleanField('收藏状态',blank=False,default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    def __str__(self):
        return str(self.id)
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客收藏列表'
        verbose_name_plural = '博客收藏列表'
