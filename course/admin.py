# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Course, Questions, PaperList, Paper, Down_info

from django.contrib import admin


# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'courseId',  'desc', 'createTime']
    list_filter = ['name', 'courseId', 'desc']
    search_fields = ['name', 'courseId']


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['course', 'questionType', 'answer', 'context', 'select_time']
    list_filter = ['course', 'questionType', 'answer', 'select_time']
    search_fields = ['course', 'questionType', 'answer', 'context', 'select_time']


class PaperListAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'is_allow', 'add_time']
    list_filter = ['course', 'name', 'is_allow', 'add_time']
    search_fields = ['course', 'name', 'is_allow', 'add_time']


class PaperAdmin(admin.ModelAdmin):
    list_display = ['course', 'paper_name', 'add_time']
    list_filter = ['course', 'paper_name', 'add_time']
    search_fields = ['course', 'paper_name', 'add_time']


class DownloadAdmin(admin.ModelAdmin):
    list_display = ['name', 'add_time']
    list_filter = ['name', 'add_time']
    search_fields = ['name', 'add_time']


admin.site.register(Course, CourseAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(PaperList, PaperListAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Down_info, DownloadAdmin)
