# -*- coding: utf-8 -*-
import xadmin
from .models import Course, Questions, PaperList, Paper, Down_info


class CourseAdmin(object):
    list_display = ['name', 'courseId',  'desc', 'createTime']
    list_filter = ['name', 'courseId', 'desc']
    search_fields = ['name', 'courseId']


class QuestionsAdmin(object):
    list_display = ['course', 'questionType', 'answer', 'context', 'select_time']
    list_filter = ['course', 'questionType', 'answer', 'select_time']
    search_fields = ['course', 'questionType', 'answer', 'context', 'select_time']


class PaperListAdmin(object):
    list_display = ['course', 'name', 'is_allow', 'add_time']
    list_filter = ['course', 'name', 'is_allow', 'add_time']
    search_fields = ['course', 'name', 'is_allow', 'add_time']


class PaperAdmin(object):
    list_display = ['course', 'paper_name', 'add_time']
    list_filter = ['course', 'paper_name', 'add_time']
    search_fields = ['course', 'paper_name', 'add_time']


class DownloadAdmin(object):
    list_display = ['name', 'add_time']
    list_filter = ['name', 'add_time']
    search_fields = ['name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Questions, QuestionsAdmin)
xadmin.site.register(PaperList, PaperListAdmin)
xadmin.site.register(Paper, PaperAdmin)
xadmin.site.register(Down_info, DownloadAdmin)