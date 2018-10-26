"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, handler404, handler500, include
from django.contrib import admin
from django.conf import settings
#
from django.views.static import serve
from .settings import MEDIA_ROOT, STATIC_URL
from django.conf.urls.static import static


from users.views import LoginView, RegisterView, UserCenterView, ModifyPwdView, LogoutView
from course.views import CourseLists, index, PaperListView, DownAddView, DownloadFunView, QuestionsView, base
from operate.views import PaperView, ChouxuanView, AddQuestionView, ScoreView, Score_Paper, \
    Change_answer_logView, Paper_Chang_QuestionView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),

    # users
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^usercenter/$', UserCenterView.as_view(), name='usercenter-info'),
    url(r'^password_reset/$', ModifyPwdView.as_view(), name='password_reset'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # index
    url(r'^$', index, name='index'),
    url(r'^base/$', base, name='base'),

    # course
    # url(r'^papersindex/$', PapersIndex.as_view(), name='papersindex'),
    url(r'^courselists/$', CourseLists, name='courselists'),
    url(r'^paperlists/$', PaperListView.as_view(), name='paperlists'),
    url(r'^questions/(?P<questions_id>.*)/$', QuestionsView.as_view(), name='questions'),
    # url(r'download_info/(?P<page_number>.*)$', DownloadFunView.as_view(), name="download"),
    # url(r'^download_add/$', DownAddView.as_view(), name='download_add'),


    # operate
    url(r'^paper/(?P<paper_id>.*)/$', PaperView.as_view(), name='paperview'),
    url(r'^chouxuan/$', ChouxuanView.as_view(), name='chouxuan'),
    url(r'^addquestion/$', AddQuestionView.as_view(), name='addquestion'),
    url(r'^change/$', QuestionsView.as_view(), name='change_question'),
    url(r'^score/$', ScoreView.as_view(), name='score'),
    url(r'^score/(?P<paper_id>.*)/$', Score_Paper.as_view(), name='score_paper'),
    url(r'changanswerlog/(?P<question_id>.*)/(?P<user_id>.*)/(?P<paper_id>.*)/(?P<course_id>.*)/$',
        Change_answer_logView.as_view(), name='chang_answer_log'),
    url(r'^paperaddquestion/(?P<paper_id>.*)/(?P<question_id>.*)/$', Paper_Chang_QuestionView.as_view(),
        name='paper_change_question'),


    # TEST
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'download_info/(?P<page_number>.*)$', DownloadFunView.as_view(), name="download"),
    url(r'downadd/$', DownAddView.as_view(), name="downadd"),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
