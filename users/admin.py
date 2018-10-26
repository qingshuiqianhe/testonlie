# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'nick_name',  'password']


admin.site.register(UserProfile, UserProfileAdmin)

