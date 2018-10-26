# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from users.models import UserProfile
from course.models import Paper, Course, PaperList, Questions


# class UserNote(models.Model):
#     # 可以删去
#     user = models.ForeignKey(UserProfile, verbose_name=u"留言人")
#     add_time = models.DateField(auto_now_add=True, verbose_name=u"留言时间")
#     note_content = models.TextField(default="", verbose_name=u"留言内容")
#
#     class Meta:
#         verbose_name = u"用户留言"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return "{0}({1})".format(self.user.nick_name, self.user.username)


class Notice(models.Model):
    pub_name = models.ForeignKey(UserProfile, verbose_name=u"发布人")
    pub_time = models.DateField(auto_now_add=True, verbose_name=u"发布时间")
    pub_content = models.TextField(verbose_name=u"通知详情")

    class Meta:
        verbose_name = u"通知发布"
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.pub_content


class UserAnswerLog(models.Model):
    """ 应该在加一个score ， 用于教师对问答题分数的提交"""
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    paper = models.ForeignKey(Paper, verbose_name=u"试卷")
    question = models.ForeignKey(Questions, verbose_name=u'题目')
    answer = models.TextField(verbose_name=u"用户答案")
    score = models.CharField(max_length=100, verbose_name=u'分数', default=0)
    add_time = models.DateField(auto_now_add=True, verbose_name=u"作答时间")

    class Meta:
        verbose_name = u"用户做题记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}({1}) ".format(self.user.nick_name, self.user.username)


class UserScore(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    paper = models.ForeignKey(PaperList, verbose_name=u"试卷")
    total = models.IntegerField(verbose_name=u"总分", default=0)
    add_time = models.DateField(verbose_name=u"录入时间", auto_now_add=True)

    class Meta:
        verbose_name = u"用户总分"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}({1}) 试卷:{2} | 总分:{3}".format(self.user.nick_name, self.user.username, self.paper.name,\
                                                 self.total)
