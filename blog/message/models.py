from django.db import models
from user.models import MyUser as User
from django.utils import timezone

# Create your models here.
class Type(models.Model):
    id = models.AutoField('序号', primary_key=True)
    type_name = models.CharField('类型名称', blank=True,default='',max_length=127)
    def __str__(self):
        return self.type_name
    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '消息类型列表'
        verbose_name_plural = '消息类型列表'

class Message(models.Model):
    id = models.AutoField('序号', primary_key=True)
    content = models.TextField('内容', blank=True,default='测试')
    time = models.DateTimeField('时间',default =timezone.now,blank = True)
    ip = models.GenericIPAddressField('ip地址',default='0.0.0.0')
    type = models.ForeignKey(Type, on_delete=models.CASCADE,verbose_name='类型')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    view = models.NullBooleanField('是否已查看',blank=True,default=0)
    def __str__(self):
        return self.content

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '消息内容列表'
        verbose_name_plural = '消息内容列表'