# -*- coding:utf-8 -*-
import random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.db.models import Q

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from .models import UserAnswerLog, UserScore, Notice
from .forms import ChouXuanForm, AddQuestionForm, QuestionFormWd, delete_questionForm, add_questionForm

from course.models import Paper, Questions, Course, PaperList, PaperSocre
from users.models import UserProfile


# 页面显示和提交判断,
class PaperView(View):

    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users

    def get(self, request, paper_id):
        # 教师得显示 和学生不一样，显示id type context 答案，
        '''
          需要改，有的东西不对
        '''
        if request.user.is_authenticated():
            user = request.user
            teachers = self.judeg_teacher()
            # user_score = UserScore.objects.get(user_id=user.id, paper_id=paper_id)
            # if user_score:
            #     msg = {'msg': u'已经参加过该课程的考试'}
            #     return render(request, 'course/paper_list.html', msg)
            # else:
            paper_list_id = PaperList.objects.filter(id=paper_id)  # 找到目标试卷
            papers = Paper.objects.filter(paper_name_id=paper_list_id)  # 找到所有试题
            question_list = []
            question_id_list = []
            for paper in papers:
                print 'paper is ', paper
                question = Questions.objects.get(pk=paper.question_id)
                question_list.append(question)
                question_id_list.append(question.id)
                # print question_id_list 获取该套试题的所有题目编号列表
            title = paper_list_id[0]
            # title = u'test'
            print 'get 方法里用户获取的题目编号为', question_id_list  # 显示当前题目编号列表
            question_now = tuple(question_list)  # 题目元组
            question_count = len(question_now)  # 题目数
            if user in teachers:
                context = {"question": question_now, "question_count": question_count, "title": title,
                           'users': teachers, 'paper_id': paper_id}
                return render(request, 'course/paper_question.html', context)
            else:
                user_score = UserScore.objects.filter(user_id=user.id, paper_id=paper_id)
                if user_score:
                    msg = {'msg': u'已经参加过该课程的考试'}
                    return render(request, 'course/paper_list.html', msg)
                if not user_score:
                    return render(request, "course/paper_question.html",
                                  {"question": question_now, "question_count": question_count, "title": title})
        else:
            return render(request, "users/login.html", {"msg": u'为保证考试客观公正，考题不对未登录用户开放'})

    def get_all_questions(self, paper_id):
        paper_list_id = PaperList.objects.filter(id=paper_id)  # 找到目标试卷
        papers = Paper.objects.filter(paper_name_id=paper_list_id)  # 找到所有试题
        question_id_list = []
        for paper in papers:
            print 'paper is ', paper
            question = Questions.objects.get(pk=paper.question_id)
            print 'question anser', question.answer
            question_id_list.append(question.id)
        return question_id_list

    def get_paper_score(self, paper_id):
        paper_socre = PaperSocre.objects.get(paper_name_id_id=paper_id)
        return paper_socre

    def judge_xz_pd(self, request, paper_id, question_id_list, xuanze_score, panduan_score):
            xz_pd_score = 0
            paper = PaperList.objects.get(id=paper_id)
            for i in question_id_list:
                user_ans = request.POST.get(str(i), '')
                question = Questions.objects.get(id=i)
                if question.answer == user_ans:
                    if question.questionType == 'xz':
                        UserAnswerLog.objects.create(user=request.user, course_id=paper.course_id, paper_id=paper.id,
                                                     question_id=question.id, answer=user_ans, score=xuanze_score)
                        xz_pd_score += xuanze_score
                    elif question.questionType == 'pd':
                        UserAnswerLog.objects.create(user=request.user, course_id=paper.course_id, paper_id=paper.id,
                                                     question_id=question.id, answer=user_ans, score=panduan_score)
                        xz_pd_score += panduan_score
                    print "试题", question.id, "答案正确"
            return xz_pd_score

    def judge_wd(self, request, paper_id, question_id_list, jianda_score):
        wd_score = 0
        paper = PaperList.objects.get(id=paper_id)
        for i in question_id_list:
            question = Questions.objects.get(id=i)
            if question.questionType == 'wd':
                user_ans = request.POST.get(str(i), '')
                answer = question.answer
                # 后端根据所提交的答案，和本身的答案进行一个相似度的比对，给出一个分数，在前台，教师根据辅助的高亮提示
                # 对系统给出的评分进行审核。记录日志，在重新写个算成成绩的
                que_score = fuzz.partial_token_set_ratio(answer, user_ans, force_ascii=False, full_process=True)
                item =que_score * jianda_score / 100
                UserAnswerLog.objects.create(user=request.user, course_id=paper.course_id, paper_id=paper.id,
                                             question_id=question.id, answer=user_ans, score=item)
                wd_score += item
        return wd_score

    def judge(self, request, paper_id):
        question_id_list = self.get_all_questions(paper_id)
        paper = PaperList.objects.get(id=paper_id)
        print 'post 方法里用户获取的题目编号为', question_id_list
        paper_score = self.get_paper_score(paper_id)
        print 'paper_score', paper_score
        xuanze_score = paper_score.xuanze_score
        panduan_score = paper_score.panduan_score
        jianda_score = paper_score.jianda_score
        print 'xz, pd,jd', xuanze_score, panduan_score, jianda_score
        temp_score = 0
        xz_pd_score = self.judge_xz_pd(request, paper_id, question_id_list, xuanze_score, panduan_score)
        wd_score = self.judge_wd(request, paper_id, question_id_list, jianda_score)
        temp_score = xz_pd_score + wd_score
        return temp_score

    def post(self, request, paper_id):
        # 教师是可以对试卷内进行修改得
        if request.user.is_authenticated():
            # 找到该用户所有的做题记录
            now_user = request.user
            teachers = self.judeg_teacher()
            if now_user in teachers:
                operate_form = delete_questionForm(request.POST)
                # ， 就是对paper<id> 内部得题得操作，删除或者添加，就這两个
                if operate_form:
                    operate = request.POST.get('operate', '')
                    question_id = request.POST.get('question_id', '')
                    if operate == 'delete':
                        delete_question = Paper.objects.filter(paper_name_id=paper_id, question_id=question_id)
                        question = Questions.objects.get(id=question_id)
                        question.select_time -= 1
                        question.save()
                        delete_question.delete()
                        msg = {'msg': u'删除成功'}
                        return render(request, 'course/paper_question.html', msg)
                    elif operate == 'add':
                        print 'add has get'
                        # 展示，对应类型的题目，供选择， 添加
                        # question = Questions.objects.get(id=question_id)
                        # course, 挑选出，类型一样的题目，当然科目页要一样
                        paper = Paper.objects.get(paper_name_id=paper_id, question_id=question_id)
                        course_id_question = paper.course_id
                        # type_question = question.questionType
                        type_question = request.POST.get('type_question', '')
                        print type_question
                        questions = Questions.objects.filter(questionType=type_question, course_id=course_id_question)
                        context = {'questions': questions, 'paper_id': paper_id}
                        return render(request, 'course/paper_question.html', context)
                else:
                    msg = {'msg': u'草屋错误'}
                    return render(request, 'course/paper_question.html', msg)
            else:
                all_score = UserScore.objects.filter(user=request.user)
                temp_score = self.judge(request, paper_id)
                user_score = UserScore()
                # 记录用户
                user_score.user = request.user
                # 记录试卷名
                user_score.paper = PaperList.objects.get(pk=paper_id)
                # 记录做题时间
                # user_score.add_time = datetime.datetime.now()
                user_score.total = temp_score
                paper = PaperList.objects.get(pk=paper_id)
                state = 0
                for i in all_score:
                    if i.paper.pk == int(paper_id):
                        state = 1
                        if temp_score > i.total:
                            i.total = temp_score
                            i.save()
                            return render(request, "users/score.html", {"score": user_score.total})
                        else:
                            return render(request, "users/score.html", {"score": user_score.total})
                if state == 0:
                    user_score.save()
                    return render(request, "users/score.html", {"score": user_score.total})


# 抽题页面操作完毕
class ChouxuanView(View):
    #  抽选数目不对得问题， 是拿出来后，判断，selevt不合格后就舍弃了，没在重新random

    def get(self, request):
        user = request.user
        users = self.judeg_teacher()
        if user in users:
            notices = Notice.objects.all()
            return render(request, 'operate/chouxuan.html', {'notices': notices})
        else:
            msg = {'msg': u'你没有权限'}
            return render(request, 'users/usercenter-info.html', msg)

    def get_middle(self):
        QuestionTypes = ('xz', 'pd', 'wd')
        middle = []
        xz_ids = []
        pd_ids = []
        wd_ids = []
        typeLength = []
        for type in QuestionTypes:
            select = []
            questions = Questions.objects.filter(questionType=type)
            typeLength.append(len(questions))
            for ques in questions:
                if ques.questionType == 'xz':
                    xz_ids.append(ques.id)
                elif ques.questionType == 'pd':
                    pd_ids.append(ques.id)
                else:
                    wd_ids.append(ques.id)
                select.append(ques.select_time)
            if isinstance(select, (list, tuple)):
                select.sort()
                n = len(select)
                m = n / 2
                if n == 0:
                    middle.append(0)
                elif n % 2 == 0:
                    middle1 = (select[m]+select[m-1])/2.0
                    middle.append(middle1)
                else:
                    middle.append(select[m])
            else:
                middle.append(False)
        # middle [xz_middle, pd_middle, wd_middle],
        # typeLength [xz_length, pd_length, wd_length]
        return [middle, typeLength, xz_ids, pd_ids, wd_ids]

    def chou_xuan(self, xuanze_num, panduan_num, jianda_num):
        get_middles = self.get_middle()
        middle = get_middles[0]
        typeLength = get_middles[1]
        xz_ids = get_middles[2]
        pd_ids = get_middles[3]
        wd_ids = get_middles[4]

        paper_ids = []
        for i in range(len(xz_ids)):
            xuanze_length = typeLength[0]
            """ 优化，简化步骤，减少运算量"""
            xuanze_select = xuanze_length - 1
            xuanze_id = random.randint(0, xuanze_select)
            print 'xuazne_id ', xuanze_id
            if xz_ids[xuanze_id] not in paper_ids:
                question = Questions.objects.filter(id=xz_ids[xuanze_id])
                if len(paper_ids) < int(xuanze_num):
                    for que in question:
                        if que.select_time <= middle[0]:
                            paper_ids.append(xz_ids[xuanze_id])
                            que.select_time += 1
                            que.save()
                        else:
                            continue
        print 'xuanze_length', len(paper_ids), paper_ids

        for i in range(len(pd_ids)):
            panduan_length = typeLength[1]
            panduan_select = panduan_length - 1
            panduan_id = random.randint(0, panduan_select)
            if pd_ids[panduan_id-1] not in paper_ids:
                question = Questions.objects.filter(id=pd_ids[panduan_id])
                if len(paper_ids) < int(xuanze_num) + int(panduan_num):
                    for que in question:
                        if que.select_time <= middle[1]:
                            paper_ids.append(pd_ids[panduan_id])
                            que.select_time += 1
                            que.save()
                        else:
                            continue
        print 'xuanze_length + panduan_length', len(paper_ids), paper_ids

        for i in range(len(wd_ids)):
            jianda_length = typeLength[2]
            jianda_select = jianda_length - 1
            jianda_id = random.randint(0, jianda_select)
            if wd_ids[jianda_select] not in paper_ids:
                question = Questions.objects.filter(id=wd_ids[jianda_id])
                if len(paper_ids) < int(xuanze_num) + int(panduan_num) + int(jianda_num):
                    for que in question:
                        if que.select_time <= middle[2]:
                            paper_ids.append(wd_ids[jianda_id])
                            que.select_time += 1
                            que.save()
                        else:
                            continue
        print 'xuanze + panduan + jianda ', len(paper_ids), paper_ids
        # paper_ids.sort()
        return paper_ids

    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users

    def post(self, request):
        chouxuan_form = ChouXuanForm(request.POST)
        # print chouxuan_form
        if chouxuan_form:  # is_valid()
            paper_name_id = request.POST.get('paper_name_id', '')
            course_id = request.POST.get('course_id', '')
            xuanze_num = request.POST.get('xuanze_num', '')
            xuanze_score = request.POST.get('xuanze_score', '')
            panduan_num = request.POST.get('panduan_num', '')
            panduan_score = request.POST.get('panduan_score', '')
            jianda_num = request.POST.get('jianda_num', '')
            jianda_score = request.POST.get('jianda_score', '')
            print xuanze_num, xuanze_score, panduan_num, panduan_score, jianda_num, jianda_score
            score = int(xuanze_num) * float(xuanze_score) + int(panduan_num) * float(panduan_score) + int(jianda_num) * float(jianda_score)
            if score != 100:
                # 修改为出题界面
                msg = {'error': u'总分错误'}
                # return HttpResponseRedirect(reverse('index'))
                return render(request, 'operate/chouxuan.html', {'error': u'总分错误'})
            else:
               paper_ids = self.chou_xuan(xuanze_num, panduan_num, jianda_num)
            paper = PaperList.objects.filter(id=paper_name_id)
            if not paper:
                PaperList.objects.create(id=paper_name_id, name=u'测试'+ paper_name_id, is_allow=True, course_id=course_id)
            for li in paper_ids:
                pap = Paper.objects.create(paper_name_id=paper_name_id, course_id=course_id, question_id=li)
                pap.save()
            #  创建根据输入对应的试题x的对应分值表单
            paper_socre = PaperSocre.objects.create(paper_name_id_id=paper_name_id, xuanze_score=xuanze_score,
                                                    panduan_score=panduan_score, jianda_score=jianda_score)
            paper_socre.save()
            return HttpResponseRedirect(reverse('paperlists'))
        else:
            msg = {'error': u'未知错误'}
            return render(request, 'operate/chouxuan.html', {'error': u'未知错误'})


# 添加题库吧还是一个form 简单一些
class AddQuestionView(View):

    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users

    def get(self, request):
        user = request.user
        teachers = self.judeg_teacher()
        if user in teachers:
            return render(request, 'operate/addquestion.html', {'teachers': teachers})
        else:
            return render(request, 'users/usercenter-info.html')

    def add(self, request,  course_id, questionType, context, answer, note='note', choice_a='choice_a',
            choice_b='choice_b', choice_c='choice_c', choice_d='choice_d', boolt='True', boolf='False'):
        question = Questions.objects.create(course_id=course_id, questionType=questionType, context=context\
                        , answer=answer, choice_a=choice_a, choice_b=choice_b, choice_c=choice_c, choice_d=choice_d\
                        , note=note, boolt=boolt, boolf=boolf)

        question.save()
        # msg = {'msg': u'添加成功'}
        # return HttpResponseRedirect(reverse('questions'))
        # return render(request, 'course/questions.html')

    def post(self, request):
        questionform = AddQuestionForm(request.POST)
        if questionform:
            operate = request.POST.get('operate', '')
            course_id = request.POST.get('course_id', '')
            questionType = request.POST.get('questionType', '')
            context = request.POST.get('context', '')
            answer = request.POST.get('answer', '')
            choice_a = request.POST.get('choice_a', '')
            choice_b = request.POST.get('choice_b', '')
            choice_c = request.POST.get('choice_c', '')
            choice_d = request.POST.get('choice_d', '')
            note = request.POST.get('note', '')
            boolt = request.POST.get('boolt', '')
            boolf = request.POST.get('boolf', '')
            if operate == 'add':
                self.add(request, course_id, questionType, context, answer, note, choice_a, choice_b, choice_c,
                         choice_d, boolt, boolf)
                msg = {'msg': u'添加成功'}
                return render(request, 'course/questions.html', msg)
            elif operate == 'select':
                questions = Questions.objects.filter(course_id=course_id, questionType=questionType,
                                                     context__contains=context)
                # return HttpResponseRedirect(reverse('questions' )))
                return render(request, 'course/questions.html', {'questions': questions})
        else:
            return HttpResponseRedirect(reversed('addquestion'))


class ScoreView(View):

    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users

    def get(self, requset):
        # 显示一个学生总分，详情不设置url， 设置url的直接跳转进去，form表达那提交去
        user = requset.user
        teachers = self.judeg_teacher()
        if user in teachers:
            context = {}
            students = UserScore.objects.all()
            print students
            context.update({'students': students, 'teachers': teachers})
            return render(requset, 'users/score.html', context)
        else:
            users = UserScore.objects.filter(user=user)
            # print user.paper.id, user.total
            # user_answer_log = UserAnswerLog.objects.filter(paper_id=paper_id)
            # paper_questions_score = PaperSocre.objects.filter(paper_name_id_id=paper_id)
            return render(requset, 'users/score.html', {'users': users})


class Score_Paper(View):
    def get(self, request, paper_id):
        # 显示出学生答案和正确答案， 简答题教师给出form, 错误合集统计
        if request.user.is_authenticated():
            teachers = self.judeg_teacher()
            now_user = request.user
            user_answer_log = UserAnswerLog.objects.filter(paper_id=paper_id)
            paper_score = PaperSocre.objects.filter(paper_name_id_id=paper_id)
            if now_user in teachers:
                students_test = UserAnswerLog.objects.filter(paper_id=paper_id)
                return render(request, 'users/score_paper.html', {'user_answer_log': user_answer_log,
                                    'teachers': teachers, 'paper_score': paper_score, 'students_test': students_test})
            else:
                user_answer_log = UserAnswerLog.objects.filter(paper_id=paper_id, user=now_user)
                return render(request, 'users/score_paper.html', {'user_answer_log': user_answer_log,
                                                                  'paper_score': paper_score})

    def judeg_teacher(self):
        users = UserProfile.objects.filter(groups__name=u'教师')
        return users


class Change_answer_logView(View):
    # 修改后提交并重新计算成绩

    def judeg_teacher(self):
        teachers = UserProfile.objects.filter(groups__name=u'教师')
        return teachers

    def get(self, request, question_id, user_id, paper_id, course_id):
        user = request.user
        teacheres = self.judeg_teacher()
        if user in teacheres:
            students_test = UserAnswerLog.objects.get(question_id=question_id, user_id=user_id, paper_id=paper_id,
                                                      course_id=course_id)
            return render(request, 'operate/change_answer_log.html', {'students': students_test})
        else:
            msg = {'msg': u'没有权限'}
            return render(request, 'users/score.html', msg)

    def post(self, request, question_id, user_id, paper_id, course_id):
        user = request.user
        teacheres = self.judeg_teacher()
        if user in teacheres:
            wd_form = QuestionFormWd(request.POST)
            if wd_form:
                score = request.POST.get('score', '')
                user_id = request.POST.get('user_id', '')
                course_id = request.POST.get('course_id', '')
                paper_id = request.POST.get('paper_id', '')
                question_id = request.POST.get('question_id', '')
                user_answer_log = UserAnswerLog.objects.get(paper_id=paper_id, user_id=user_id, course_id=course_id,
                                                            question_id=question_id)

                new_user_score = UserScore.objects.get(paper_id=paper_id, user_id=user_id)
                """ 先减后加对于改变得分数"""
                print new_user_score.total, '-', user_answer_log.score
                new_user_score.total -= float(user_answer_log.score)
                print new_user_score.total, '-111', score
                user_answer_log.score = float(score)
                user_answer_log.save()
                new_user_score.total += user_answer_log.score
                new_user_score.save()

                msg = {'msg': u'修改成功'}
                return render(request, 'users/score_paper.html', msg)
        else:
            msg = {'msg': u'没有权限'}
            return render(request, 'users/score_paper.html', msg)


class Paper_Chang_QuestionView(View):

    def judeg_teacher(self):
        teachers = UserProfile.objects.filter(groups__name=u'教师')
        return teachers

    def get(self, request, paper_id, question_id):
        if request.user.is_authenticated:
            user = request.user
            teachers = self.judeg_teacher()
            if user in teachers:
                question = Questions.objects.get(id=question_id)
                context = {'question': question, 'paper_id': paper_id}
                return render(request, 'operate/paper_add_question.html', context)
            else:
                msg = {'msg': u'没有权限'}
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, paper_id, question_id):
        question = Questions.objects.get(id=question_id)
        Paper.objects.create(paper_name_id=paper_id, question_id=question_id, course_id=question.course_id)
        question.select_time += 1
        question.save()
        msg = {'mas': u'添加成功'}
        # return HttpResponseRedirect(reversed('paperview'))
        # return render_to_response('course/paper_question.html', {'paper_id': paper_id, 'msg': msg})
        return render(request, 'course/paper_list.html', msg)


class NoticeView(View):

    def get(self, request):
        notices = Notice.objects.all()
        print notices
        return render(request, 'base.html', {'notices': notices})
