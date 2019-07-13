#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: User.py
@time: 2019/7/4 18:11'''

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
# define profile.json constant, the file is used to
# save user name and password_hash
PROFILE_FILE = "profiles.json"


class User(UserMixin):

    def __init__(self, username):
        self.id = username
        self.username = username
        is_first_login = False
        ran = 0

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
