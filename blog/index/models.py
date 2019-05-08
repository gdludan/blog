from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from user.models import MyUser as User
# Create your models here.


class ArticleManager(models.Manager):
    def distinct_date(self):  # 该管理器定义了一个distinct_date方法，目的是找出所有的不同日期
        distinct_date_list = []  # 建立一个列表用来存放不同的日期 年-月
        date_list = self.values('time').order_by(
            '-time')  # 根据文章字段time找出所有文章的发布时间
        for date in date_list:  # 对所有日期进行遍历，当然这里会有许多日期是重复的，目的就是找出多少种日期
            date = date['time'].strftime('%Y{}%m{}  {}').format('年', '月', '归档')
            # 取出一个日期改格式为 ‘xxx年/xxx月 归档’
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


class Post(models.Model):
    ORIGINAL = '原创'
    REPRINT = '转载'
    TALK = '杂谈'
    Tutorial = "指南"
    id = models.AutoField('序号', primary_key=True)
    title = models.CharField('标题', max_length=255, default='')
    content = HTMLField('内容', default='')
    type = models.CharField(
        '类型', max_length=8, default=ORIGINAL, choices=(
            (ORIGINAL, '原创'), (REPRINT, '转载'), (TALK, '杂谈'), (Tutorial, "指南")))
    time = models.DateTimeField('创建时间', max_length=125, default=timezone.now)
    readnumber = models.IntegerField('阅读数量', default=0)
    Prohibited = models.NullBooleanField('禁止查看', blank=False, default=0)
    Prohibited_info = models.CharField(
        '禁止信息', blank=False, default='违规', max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    objects = ArticleManager()  # 在模型中使用自定义的管理器

    def __str__(self):
        return self.title

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客文章列表'
        verbose_name_plural = '博客文章列表'


class Comment(models.Model):
    id = models.AutoField('序号', primary_key=True)
    content = HTMLField('内容')
    time = models.DateTimeField(
        '时间', max_length=128, auto_now_add=timezone.now)
    Prohibited = models.NullBooleanField('禁止查看', blank=False, default=0)
    Prohibited_info = models.CharField(
        '禁止信息', blank=False, default='违规', max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    reply = []

    def __str__(self):
        return self.content

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客评论列表'
        verbose_name_plural = '博客评论列表'


class Reply(models.Model):
    id = models.AutoField('序号', primary_key=True)
    content = HTMLField('内容')
    time = models.DateTimeField(
        '时间', max_length=128, auto_now_add=timezone.now)
    Prohibited = models.NullBooleanField('禁止查看', blank=False, default=0)
    Prohibited_info = models.CharField(
        '禁止信息', blank=False, default='违规', max_length=256)
    reply_id = models.IntegerField("回复列表ID", default=0)
    to_user = models.IntegerField("回复用户ID", default=0)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return self.content

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客回复列表'
        verbose_name_plural = '博客回复列表'


class Tags(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('名称', max_length=125, default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客标签列表'
        verbose_name_plural = '博客标签列表'


class Dynamic(models.Model):
    id = models.AutoField('序号', primary_key=True)
    dynamic_like = models.IntegerField('点赞次数', blank=True, default=0)
    dynamic_collection = models.IntegerField('收藏次数', blank=True, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.post.title

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客动态列表'
        verbose_name_plural = '博客动态列表'


class Like(models.Model):
    id = models.AutoField('序号', primary_key=True)
    is_like = models.NullBooleanField('点赞状态', blank=False, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return str(self.id)

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客点赞列表'
        verbose_name_plural = '博客点赞列表'


class Collection(models.Model):
    id = models.AutoField('序号', primary_key=True)
    is_collection = models.NullBooleanField('收藏状态', blank=False, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return str(self.id)

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '博客收藏列表'
        verbose_name_plural = '博客收藏列表'


class Message(models.Model):
    id = models.AutoField('序号', primary_key=True)
    username = models.CharField('用户名', max_length=127)
    title = models.CharField('标题', max_length=256)
    content = models.TextField('内容', max_length=512)
    publish = models.DateTimeField('留言时间', auto_now_add=timezone.now)

    def __str__(self):
        tpl = '<Message:[username={username}, title={title}, content={content}, publish={publish}]>'
        return tpl.format(
            username=self.username,
            title=self.title,
            content=self.content,
            publish=self.publish)

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '留言信息列表'
        verbose_name_plural = '留言信息列表'
