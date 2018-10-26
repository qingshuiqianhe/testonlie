# -*- coding: utf-8 -*-
import xadmin
from .models import Notice, UserAnswerLog, UserScore


class NoticeAdmin(object):
    list_display = ['pub_name', 'pub_content', 'pub_time']
    search_fields = ['pub_name__username', 'pub_name__nick_name', 'pub_content']
    list_filter = ['pub_name', 'pub_content', 'pub_time']


class UserAnswerLogAdmin(object):
    list_display = ['user', 'course', 'question',  'paper', 'answer', 'add_time']
    search_fields = ['user__nick_name', 'user__username', 'paper__paper_name', 'answer']
    list_filter = ['user', 'paper', 'answer', 'add_time']


class UserScoreAdmin(object):
    list_display = ['user', 'paper', 'total', 'add_time']
    search_fields = ['user__nick_name', 'user__username', 'paper__paper_name', 'total']
    list_filter = ['user', 'paper', 'total','add_time']


xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(UserAnswerLog, UserAnswerLogAdmin)
xadmin.site.register(UserScore, UserScoreAdmin)