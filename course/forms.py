# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django import forms


class ChangeForm(forms.Form):
    context = forms.Textarea()
    answer = forms.Textarea()


