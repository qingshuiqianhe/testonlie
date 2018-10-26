# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django import forms


class QuestionFormWd(forms.Form):
    user_id = forms.CharField()
    course_id = forms.CharField()
    paper_id = forms.CharField()
    score = forms.CharField()
    question_id = forms.CharField()


class AddQuestionForm(forms.Form):
    operate = forms.ChoiceField(choices=(('add', u"添加题"), ('delete', u'删除题'), ('change', u'修改'), ('select', u'查找')))
    course_id = forms.IntegerField()
    questionType = forms.ChoiceField(choices=(("xz", u"选择"), ("pd", u"判断"), ('wd', u"问答")))
    context = forms.Textarea()
    answer = forms.Textarea()
    choice_a = forms.Textarea()
    choice_b = forms.Textarea()
    choice_c = forms.Textarea()
    choice_d = forms.Textarea()
    note = forms.Textarea()
    boolt = forms.Textarea()
    boolf = forms.Textarea()


class ChouXuanForm(forms.Form):
    xuanze_num = forms.IntegerField(min_value=0)
    xuanze_score = forms.FloatField(min_value=1)
    panduan_num = forms.IntegerField(min_value=0)
    panduan_score = forms.FloatField(min_value=1)
    jianda_num = forms.IntegerField(min_value=0)
    jianda_score = forms.FloatField(min_value=1)


class delete_questionForm(forms.Form):
    question_id = forms.CharField()
    operate = forms.CharField()
    type_question = forms.CharField()


class add_questionForm(forms.Form):
    question_id = forms.CharField()
    operate = forms.CharField()




