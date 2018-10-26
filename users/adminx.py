# -*- coding: utf-8 -*-
import xadmin
from .models import UserProfile, FileStroes


class UserProfileAdmin(object):
    list_display = ['username', 'nick_name',  'password']


class FileStoreAdmin(object):
    list_display = ['file_name', 'add_time', 'file_content']


# xadmin.site.register(UserProfileAdmin)
xadmin.site.register(FileStroes, FileStoreAdmin)
