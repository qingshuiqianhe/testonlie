# -*- coding: utf-8 -*-
import random, os
from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.generic.base import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from blogproject.settings import MEDIA_URL, MEDIA_ROOT, BASE_DIR

from users.models import UserProfile

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Course, Questions, PaperList, Paper
from .forms import ChangeForm
from users.models import FileStroes
from operate.models import UserScore, Notice
from users.forms import UploadFileForm

context = {}


# 单独的试题，的修改删除逻辑， 已完成
class QuestionsView(View):

    def judeg_teacher(self):
        teachers = UserProfile.objects.filter(groups__name=u'教师')
        return teachers

    def get(self, request, questions_id):
        user = request.user
        teachers = self.judeg_teacher()
        title = {'title': u'问题详情'}
        if user in teachers:
            question = Questions.objects.get(id=questions_id)
            return render(request, 'operate/change.html', {'question': question, 'title': title})
        else:
            msg = {'msg': u'没有权限'}
            return render(request, 'users/usercenter-info.html', msg)

    def post(self, request,  questions_id):
        questions = Questions.objects.get(id=questions_id)
        changeForm = ChangeForm(request.POST)
        if changeForm:
            delete = request.POST.get('delete', '')
            if delete:
                questions.delete()
                return HttpResponseRedirect(reverse('addquestion'))
                # return render(request, 'course/questions.html', {'msg': u'删除成功'})
            change = request.POST.get('change', '')
            if change:
                context = request.POST.get('context', '')
                answer = request.POST.get('answer', '')
                questions.context = context
                questions.answer = answer
                questions.save()
            return render(request, 'operate/change.html', {'questions': questions, 'msg': u'修改成功'})
        else:
            return render(request, 'operate/addquestion.html', {'msg': "错误操作"})


def CourseLists(request):
    courseList = Course.objects.all()

    return render(request, 'course/allcourse.html', {'courseList': courseList, 'title': u'全部课程'})


class PaperListView(View):
    """试题列表页面"""
    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users

    def get(self, request):
        if request.user.is_authenticated():
            user = request.user
            papers = PaperList.objects.filter(is_allow=True)
            print papers
            teachers = self.judeg_teacher()
            notices = Notice.objects.all()
            context = {}
            context.update({'title':  u"试题列表页面"})
            context.update({'papers': papers, 'teachers': teachers, 'notices': notices})
            if user in teachers:
                return render(request, 'course/paper_list.html', context)
            else:
                not_done = []
                dong = []
                for paper in papers:
                    dong_papers = UserScore.objects.filter(paper_id=paper.id, user_id=user.id)
                    if not dong_papers:
                        not_done.append(paper)
                    else:
                        dong.append(dong_papers)
                if len(not_done) == 0:
                    context.update({'msg': u'没有未完成的试卷'})
                    context.update({'papers_done': dong})
                    return render(request, "course/paper_list.html", context)
                else:
                    print not_done
                    context = {"papers_done": dong, "title": u"试题列表页面", 'papers_not_done': not_done}
                    return render(request, "course/paper_list.html", context)
        else:
            msg = {'msg': u'请登陆'}
            return render(request, 'users/login.html', msg)


class DownloadFunView(View):
    def get(self, request, page_number):
        file_list = FileStroes.objects.all()
        print 'page_number', page_number

        return render(request, "course/download.html", {"file_list": file_list})


def handle_uploaded_file(f):
    with open('media/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class DownAddView(View):
    def post(self, request):
        print 'meida root', MEDIA_ROOT
        # form = UploadFileForm(request.POST, request.FILES)
        # # handle_uploaded_file(request.FILES['fileUpload'])
        # file = request.FILES['fileUpload']
        # file_test = '%s/%s' % (settings.MEDIA_ROOT, file.name)
        # print file_test
        # file_id = request.POST.get("fileUpload")
        #
        # print "asdfsasdfasdf", file.name, file_id
        # # path = default_storage.save(file_id, ContentFile(file_id.read()))

        obj = request.FILES.get('fileUpload')
        path = '%s/%s' % ('/media', obj.name)
        print 'path', path
        f = open(os.path.join('/media/', obj.name), 'wb')
        print f
        for line in obj.chunks():
            f.write(line)
        f.close()
        FileStroes.objects.create(file_name=obj.name, file_content=path)
        file_list = FileStroes.objects.all()
        return render(request, "course/download.html", {"file_list": file_list})


# 首页
def index(request):
    context = {}

    notices = Notice.objects.all()
    context.update({'notices': notices})
    context.update({'title': u'在线考试系统'})

    return render(request, 'index.html', context)


def base(request):
    teachers = UserProfile.objects.filter(groups__name=u'教师')
    notices = Notice.objects.all()
    msg = {'notices': notices, 'teachers': teachers}
    return render(request, 'base.html', msg)






# for li in list:
#     pap = Paper.objects.create(paper_name_id = 1, course_id= 1, question_id= li)
"""
选中次数得数组
[6, 5, 2, 6, 2, 10, 7, 4, 7, 4, 5, 5, 5, 6, 1, 5, 9, 11, 5, 8, 6, 6, 5, 5, 4, 3, 7, 3, 3, 3, 8, 1, 3, 3, 6, 6, 6, 2, 9,
4, 3, 4, 8, 4, 2, 5, 4, 8, 7, 6, 5, 6, 7, 5, 4, 5, 4, 10, 3, 4, 3, 4, 8, 3, 7, 8, 6, 5, 3, 6, 2, 3, 4, 6, 3, 7, 6, 4, 4,
5, 8, 3, 3, 7, 5, 5, 4, 5, 2, 2, 3, 6, 2, 2, 7, 3, 8, 7, 3, 3, 3, 4, 4, 4, 6, 4, 6, 3, 3, 7, 4, 6, 2, 2, 4, 4, 8, 5, 5,
1, 3, 5, 11, 3, 4, 7, 4, 5, 2, 4, 7, 2, 6, 5, 5, 2, 5, 4, 1, 5, 1, 3, 6, 6, 7, 7, 3, 2, 6, 4, 5, 5, 5, 7, 8, 3, 9, 8, 2,
3, 5, 6, 6, 6, 3, 5, 8, 4, 5, 7, 6, 5, 7, 8, 5, 6, 6, 4, 6, 9, 5, 4, 7, 1, 5, 8, 2, 7, 6, 3, 1, 4, 2, 4, 5, 6, 3, 6, 6,
9, 3, 5, 3, 5, 6, 3, 4, 2, 6, 4, 7, 9, 1, 3, 4, 6, 13, 3, 4, 5, 9, 6, 6, 7, 5, 3, 5, 6, 6, 5, 4, 8, 5, 3, 7, 3, 4, 6, 2,
5, 3, 1, 8, 3, 4, 6, 4, 2, 5, 3, 9, 3, 8, 2, 4, 3, 5, 4, 7, 3, 8, 1, 4, 8, 4, 4, 7, 3, 5, 4, 5, 6, 5, 7, 5, 5, 6, 4, 3,
6, 4, 7, 2, 4, 6, 8, 3, 4, 6, 6, 4, 9, 11, 4, 3, 4, 6, 7, 2, 2, 0, 4, 8, 2, 5, 12, 4, 3, 6, 6, 5, 5, 7, 6, 5, 6, 2, 6, 6,
4, 9, 4, 5, 4, 2, 5, 1, 8, 10, 4, 6, 6, 2, 7, 3, 2, 4, 9, 8, 5, 6, 7, 6, 6, 0, 4, 6, 8, 5, 3, 7, 3, 7, 5, 5, 7, 4, 4, 8,
4, 2, 6, 6, 5, 6, 6, 2, 9, 4, 2, 1, 8, 4, 10, 2, 4, 3, 7, 5, 5, 8, 4, 5, 5, 0, 6, 5, 8, 3, 2, 5, 3, 5, 7, 6, 2, 7, 4, 7,
4, 10, 4, 6, 5, 6, 5, 4, 4, 3, 5, 5, 6, 3, 4, 3, 4, 3, 5, 4, 5, 6, 6, 2, 9, 6, 4, 4, 4, 4, 2, 7, 5, 3, 4, 8, 5, 7, 1, 3,
8, 5, 5, 5, 7, 7, 8, 5, 5, 4, 4, 5, 4, 6, 4, 3, 6, 3, 10, 6, 5, 3, 8, 2, 8, 3, 9, 2, 3, 5, 5, 1, 4, 4, 7, 7, 8, 7, 4, 2,
3, 2, 5, 3, 4, 5, 3, 6, 6, 4, 6, 2, 6, 4, 1, 7, 6, 9, 6, 6, 5, 4, 3, 3, 6, 3, 4, 3, 4, 5, 5, 8, 4, 7, 4, 3, 2, 5, 6, 4,
7, 6, 6, 7, 4, 4, 6, 4, 5, 2, 7, 3, 4, 8, 7, 8, 3, 3, 8, 5, 7, 5, 4, 0, 5, 4, 5, 7, 1, 2, 3, 9, 4, 7, 2, 6, 5, 8, 3, 5,
3, 5, 8, 1, 7, 7, 7, 7, 5, 2, 5, 4, 9, 7, 3, 4, 3, 3, 5, 7, 2, 8, 6, 4, 2, 7, 9, 10, 4, 6, 7, 7, 4, 4, 6, 6, 7, 3, 4, 4,
7, 4, 3, 6, 4, 4, 6, 4, 4, 3, 3, 6, 5, 7, 5, 6, 4, 3, 3, 4, 2, 3, 6, 5, 4, 1, 7, 3, 1, 2, 8, 3, 2, 6, 6, 6, 8, 5, 3, 7,
3, 6, 10, 2, 5, 10, 7, 2, 3, 6, 2, 6, 7, 6, 8, 9, 7, 6, 4, 6, 10, 2, 5, 2, 4, 3, 5, 8, 1, 1, 2, 9, 6, 3, 5, 4, 3, 7, 7,
7, 10, 8, 5, 3, 4, 2, 1, 5, 5, 4, 4, 7, 2, 4, 6, 3, 4, 8, 4, 2, 7, 5, 5, 5, 8, 5, 6, 7, 7, 3, 3, 5, 9, 7, 7, 7, 6, 9, 5,
4, 5, 7, 3, 6, 5, 2, 3, 7, 7, 3, 5, 8, 6, 3, 3, 7, 1, 4, 6, 7, 7, 3, 4, 10, 5, 2, 6, 4, 6, 7, 4, 6, 5, 4, 3, 4, 3, 5, 1,
8, 2, 3, 4, 6, 7, 3, 5, 6, 8, 6, 6, 2, 4, 2, 6, 8, 4, 5, 7, 5, 3, 2, 4, 6, 5, 8, 8, 6, 6, 1, 7, 3, 4, 7, 5, 9, 4, 10, 5,
5, 6, 6, 5, 9, 3, 5, 8, 5, 4, 4, 5, 2, 4, 5, 5, 6, 6, 5, 10, 3, 5, 3, 6, 6, 5, 7, 5, 8, 3, 4, 5, 2, 7, 7, 5, 3, 4, 2, 5,
3, 6, 6, 3, 6, 12, 3, 4, 4, 8, 7, 3, 6, 8, 6, 4, 6, 6, 4, 5, 3, 3, 9, 10, 7, 10, 5, 4, 2, 7, 4, 3, 4, 5, 3, 2, 2, 6, 2,
3, 7, 3, 7, 6, 5, 7, 1, 6, 4, 9, 4, 3, 5, 10, 4, 9, 3, 2, 3, 9, 7, 7, 6, 7, 0, 6, 9, 2, 4, 2, 7, 5, 7, 1, 8, 2, 9, 5, 8,
3, 3, 7, 5, 3, 5, 4, 4, 4, 4, 3, 8, 2, 7, 7, 7, 1, 2, 6, 4, 4, 5, 4, 1, 6, 2, 4, 5, 5, 4, 5, 3, 4, 6, 7, 3, 6, 5, 4, 5,
4, 2, 3, 5, 4, 2, 2, 6, 3, 4, 3, 1, 8, 7, 5, 7, 4, 8, 1, 5, 4, 2, 5, 4, 5, 8, 7, 6, 7, 6, 8, 6, 4, 6, 4, 3, 8, 7, 6, 4,
5, 5, 8]
"""
"""
抽中次数，对应得题目数量： 一次没抽中得有2个
>>> print max(select)
13
>>> for i in range(14):
...     print i, select.count(i)
...
0 5
1 31
2 86
3 143
4 178
5 168
6 153
7 116
8 67
9 30
10 17
11 3
12 2
13 1
[{0: 5}, {1: 31}, {2: 86}, {3: 143},{4: 178},{5: 168}, {6: 153}, {7: 116}, {8: 67},{9: 30},{10: 17}, {11: 3},  {12: 2},
{13: 1}]
中位数：后期加判断 ，大于中位数重新random
>>> get_middle(select)
u'5.000000'
"""

