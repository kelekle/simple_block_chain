#!/usr/bin/env python
# encoding: utf-8
'''
@author: kle
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: database.py
@time: 2019/7/2 23:28'''

import threading
import pymysql

class DataBase(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="kle", passwd="yqyforever", db="block_chain")

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with DataBase._instance_lock:
                if not hasattr(cls, '_instance'):
                    DataBase._instance = DataBase(*args, **kwargs)
        return DataBase._instance

    def get_db(self):
        return self.db
