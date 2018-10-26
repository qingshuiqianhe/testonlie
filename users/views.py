# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password


# Create your views here.
from .forms import LoginForm, RegisterForm, UserInfoForm, ModifyPwdForm, UploadFileForm
from .models import UserProfile



# class CustomBackend(ModelBackend):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#             user = UserProfile.objects.get(Q(username=username))  #可以使用用户名和Email登录
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None

# 登陆
class LoginView(View):
    def get(self, request):
        title = {'title': u'登陆'}
        return render(request, 'users/login.html', title)

    def post(self, request):
        longin_form = LoginForm(request.POST)
        if longin_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('usercenter-info'))
                    # return render(request, 'users/usercenter-info.html', {'username': user.username})
                else:
                    return render(request, 'users/login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'users/login.html', {'login_form': longin_form})


# 注册
class RegisterView(View):
    def get(self, request):
        title = {'title': u'注册'}
        return render(request, 'users/register.html', title)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': "用户已存在"})
            pass_word = request.POST.get('password', '')
            user = UserProfile()
            user.username = user_name
            # user.password = pass_word
            user.password = make_password(pass_word)
            user.save()
            return render(request, 'users/login.html')
        else:
            return render(request, 'users/register.html', {'register_form': register_form})


# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserCenterView(View):

    def get(self, request):
        title = u'用户中心'
        user = request.user
        user_form = UserInfoForm()
        user_form.nick_name = user.nick_name
        user_form.birthday = user.birthday
        user_form.institute = user.institute
        user_form.gender = user.gender
        user_form.mobile = user.mobile
        user_form.institute = user.institute
        return render(request, "users/usercenter-info.html", {"user_form": user_form, "title": title})

    def post(self, request):
        changeInfoFrom = UserInfoForm(request.POST)
        user = request.user
        if changeInfoFrom:
            nick_name = request.POST.get('nick_name', '')
            birthday = request.POST.get('birthday', '')
            institute = request.POST.get('institute', '')
            gender = request.POST.get('gender', '')
            mobile = request.POST.get('mobile', '')
            user.nick_name = nick_name
            user.birthday = birthday
            user.institute = institute
            user.gender = gender
            user.mobile = mobile
            user.save()
            msg = {'msg': u'修改成功'}
        else:
            msg = {'msg': u'修改失败'}
        return render(request, 'users/usercenter-info.html', msg)


# reset paaword ok
class ModifyPwdView(View):
    def get(self, request):
        title = {'title': u'重置密码'}
        return render(request, 'users/password_reset.html', title)

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"msg": "两次输入的密码不相同"})
                pass
            # user = UserProfile.objects.get(email=email)
            user = request.user
            user.password = make_password(password=pwd1)
            user.save()
            return render(request, "users/usercenter-info.html", {"msg": "密码修改成功"})
        else:
            # email = request.POST.get("email", "")
            return render(request, "users/password_reset.html", {"modify_form": ""})


# 404调试
def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'course/download.html', {'form': form})


# 500调试
def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response


