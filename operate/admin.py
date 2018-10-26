from django.contrib import admin

# Register your models here.
from .models import Notice, UserAnswerLog, UserScore


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['pub_name', 'pub_content', 'pub_time']
    search_fields = ['pub_name__username', 'pub_name__nick_name', 'pub_content']
    list_filter = ['pub_name', 'pub_content', 'pub_time']


class UserAnswerLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'question',  'paper', 'answer', 'add_time']
    search_fields = ['user__nick_name', 'user__username', 'paper__paper_name', 'answer']
    list_filter = ['user', 'paper', 'answer', 'add_time']


class UserScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'paper', 'total', 'add_time']
    search_fields = ['user__nick_name', 'user__username', 'paper__paper_name', 'total']
    list_filter = ['user', 'paper', 'total','add_time']


admin.site.register(Notice, NoticeAdmin)
admin.site.register(UserAnswerLog, UserAnswerLogAdmin)
admin.site.register(UserScore, UserScoreAdmin)
