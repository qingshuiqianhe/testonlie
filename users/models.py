# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


"""pbkdf2_sha256$24000$rw9ulAokR1eY$PK43kJEuqfSz/JGQWpXrEM8iPhaYneqEaE7gHPGtRTY="""


class UserProfile(AbstractUser):
    """username作为工号或者学号使用，排除id这种定西， 以下定义老师，学生继承,不想继承了，后台分组把"""
    nick_name = models.CharField(max_length=50, verbose_name=u'名字', default='')
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', '女')), default='male')
    institute = models.CharField(max_length=50, verbose_name=u"学院", default=u"信息学院")
    birthday = models.DateField(max_length=8, verbose_name=u"生日", null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="static/images/head/", default="static/images/head/default.png",
                              max_length=100)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
        db_table = 'UserProfile'

    def __unicode__(self):
        return '{0}({1})'.format(self.username, self.nick_name)


class FileStroes(models.Model):
    """文件管理，上传共享资料"""
    file_name = models.CharField(max_length=100, verbose_name=u"文件名")
    file_content = models.FileField(verbose_name=u"文件", upload_to="file/%Y/%m/%d")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u"发布时间")
    down_count = models.IntegerField(default=0, verbose_name=u"下载次数")

    class Meta:
        verbose_name = u"资料下载管理"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
        db_table = 'FileStroes'

    def __unicode__(self):
        return '{0}({1})'.format(self.file_name, self.down_count)





