# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client

from .views import *
from .models import *

class userTestcase(TestCase):
    def setUp(self):
        UserProfile.objects.create(nick_name='xxx'
                                   )
        return UserProfile.objects.all()
    def test_index(self):
        response = self.client.get('/')


class SendViewsTestCase(TestCase):
    def setUp(self):
        print 'xxxx'

    def test_creat_sms(self):
        c = Client()
        rep = c.get('/')
        print rep

if __name__ == '__main__':
    aa = SendViewsTestCase()
    aa.test_creat_sms()