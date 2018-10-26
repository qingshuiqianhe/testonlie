# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    courseId = models.CharField(max_length=20, verbose_name=u"课程号", default='hcs0000')
    desc = models.CharField(max_length=400, verbose_name=u"课程说明", blank=True)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
        ordering = ['-createTime']
        db_table = 'course'

    def __unicode__(self):
        return self.name


class Questions(models.Model):
    #  问题不设置分数，后期认为设置出题的时候判断
    course = models.ForeignKey(Course, verbose_name=u"课程")
    questionType = models.CharField(max_length=2, choices=(("xz", u"选择"), ("pd", u"判断"), ('wd', u"问答")),\
                                    verbose_name=u"题目类型")
    context = models.TextField(verbose_name=u"题目内容")
    answer = models.TextField(verbose_name=u"正确答案")
    choice_a = models.TextField(verbose_name=u"A选项", default="A.我是答案A")
    choice_b = models.TextField(verbose_name=u"B选项", default="B.我是答案B")
    choice_c = models.TextField(verbose_name=u"C选项", default="C.我是答案C")
    choice_d = models.TextField(verbose_name=u"D选项", default="D.我是答案D")
    note = models.TextField(verbose_name=u"备注信息", default=u"问答题在此处做答")
    boolt = models.TextField(verbose_name=u"判断正误正确选项", default="True")
    boolf = models.TextField(verbose_name=u"判断正误错误选项", default="False")
    add_time = models.DateField(auto_now_add=True, verbose_name=u"添加时间")
    select_time = models.IntegerField(verbose_name=u'选中次数', default=0)
    # rate = models.FloatField(verbose_name=u'选中频率', default=0.0)

    class Meta:
        verbose_name = u"题库"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
        db_table = 'questions'

    @property
    def get_context_display(self):
        return self.context

    @property
    def get_question_id(self):
        return self.id

    def __unicode__(self):
        return "{0}(题干:{1} | 正确答案:{2} )".format(self.course.name, self.context, self.answer)

    def __str__(self):
        return "{0}(题干:{1} | 正确答案:{2} )".format(self.course.name, self.context, self.answer)


class PaperList(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"所属课程")
    name = models.CharField(max_length=100, verbose_name=u"试卷名", default=u"")
    is_allow = models.BooleanField(default=False, verbose_name=u"是否启用")
    add_time = models.DateField(auto_now_add=True, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"试卷列表"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
        db_table = 'PaperLists'

    def __unicode__(self):
        return u"{0}(试卷名称:{1} | 使用状态:{2})".format(self.course.name, self.name, self.is_allow)


class Paper(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"所属课程", default=1)
    question = models.ForeignKey(Questions, verbose_name=u"题目")
    paper_name = models.ForeignKey(PaperList, verbose_name=u"试卷名称")
    add_time = models.DateField(auto_now_add=True, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"试题列表"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
        db_table = 'paper'

    def __unicode__(self):
        return u"{0} ({1})".format(self.paper_name, self.question.context)


class Down_info(models.Model):
    # 资料下载页面
    name = models.CharField(verbose_name=u"资料名", default=u"资料", max_length=100)
    add_time = models.DateField(verbose_name=u"添加时间", auto_now_add=True)
    file = models.FileField(verbose_name=u"文件")

    class Meta:
        verbose_name = u"资料下载"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
        # db_table = 'FileStroes'

    def __unicode__(self):
        return self.name


class PaperSocre(models.Model):
    paper_name_id = models.ForeignKey(PaperList, verbose_name=u'所属试卷分值')
    xuanze_score = models.FloatField(verbose_name=u'选择分值', blank=True)
    panduan_score = models.FloatField(verbose_name=u'判断分值', blank=True)
    jianda_score = models.FloatField(verbose_name=u'简答分值', blank=True)

    class Meta:
        verbose_name = u"试卷分值表"
        verbose_name_plural = verbose_name
        ordering = ['id']
