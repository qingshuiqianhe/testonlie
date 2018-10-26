# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class UserInfoForm(forms.Form):
    nick_name = forms.CharField(required=True, max_length=20)
    institute = forms.CharField(max_length=50)
    birthday = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=(("male", u"男"), ("female", u"女")), required=True)
    mobile = forms.CharField(required=True, max_length=11)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


