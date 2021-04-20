#!/usr/bin/env python
# encoding: utf-8
'''
@author: kle
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: dbaction.py
@time: 2019/7/3 0:25'''

import traceback
import pymysql
from db.database import DataBase

class DBAction():
    #连接池对象
    def __init__(self):
        global db_instance
        db_instance = None
        if db_instance == None:
            db_instance = DataBase.instance()
        # 建立和数据库系统的连接
        self.conn = db_instance.get_db()
        #获取操作游标
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_database(self):
        self.cursor.close()
        self.conn.close()

    def operate(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :param database:
        :param sql:
        :return: 成功：0，失败：1
        '''
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            return 0
        except:
            print("sql is %s, params is %s error. %s" % (sql, params, traceback.format_exc()))
            self.conn.rollback()
            raise Exception

    def data_operate_many(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :param sql:
        :param params:
        :return: 成功：0，失败：1
        '''
        #执行sql语句
        self.cursor.executemany(sql, params)
        #提交到数据库执行
        self.conn.commit()

    def data_operate_count(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :return: 受影响的条数
        '''
        #执行sql语句
        count = self.cursor.execute(sql, params)
        #提交到数据库执行
        self.conn.commit()
        return count

    def inquery(self, sql, params=()):
        '''
        :param database:
        :param sql:
        :return: ((),(),...,())
        '''
        # print(sql)
        self.cursor.execute(sql, params)
        self.conn.commit()
        result = self.cursor.fetchone()
        # print(result)
        if result is None:
            return -1
        else:
            return result


    def get_info(self, sql, params=()):
        '''
                :param database:
                :param sql:
                :return: ((),(),...,())
                '''
        # print(sql)
        self.cursor.execute(sql, params)
        self.conn.commit()
        result = self.cursor.fetchone()
        if result is None:
            return -1
        else:
            return result

    def data_inquiry_all(self, sql, params=()):
        '''
        :param database:
        :param sql:
        :return: ((),(),...,())
        '''
        self.cursor.execute(sql, params)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.conn.commit()
