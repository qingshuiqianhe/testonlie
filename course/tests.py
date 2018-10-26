# -*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.
from course.models import Questions


from django.db.models import Q


class CourseTest(TestCase):
    def test_question(self):
        questions = Questions.objects.filter(questionType='wd').exclude(Q(answer__contains=u'通信') | Q(answer__contains=u'分布计算'))
        print questions

if __name__ == "__main__":
    course = CourseTest
    course.test_question()