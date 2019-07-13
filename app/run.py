#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: run.py
@time: 2019/7/13 11:12'''

from app import app, login_manager
import os
from controller.nodelist import *
from flask_wtf import CSRFProtect

if __name__ == "__main__":
    login_manager.init_app(app)
    app.secret_key = os.getenv('SECRET_KEY', 'secret string')
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.debug = True

    # csrf protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    login = Login()
    CompleteList.HALF_USER_NUM = login.get_user_nums() / 2
    handler1 = CompleteList(2, "Thread-2", 1)
    handler1.start()
    handler2 = LoginList(3, "Thread-3", 1)
    handler2.start()
    app.run(use_reloader=False)
    # app.run(host="0.0.0.0", use_reloader=False)
    # app.run(debug=True, use_reloader=False, threaded=True)
