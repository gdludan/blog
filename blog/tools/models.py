from django.db import models
from django.utils import timezone


class Access(models.Model):
    id = models.AutoField('序号', primary_key=True)
    date = models.DateTimeField('日期', default=timezone.now, max_length=125)
    num = models.IntegerField('访问量', default=0)

    def __str__(self):
        return self.num

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '网站访问量列表'
        verbose_name_plural = '网站访问量列表'


class SetCtarl(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('名称', max_length=125, default="")
    is_start = models.BooleanField('是否开启', default=False)

    def __str__(self):
        return self.name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '网站设置控制列表'
        verbose_name_plural = '网站设置控制列表'
