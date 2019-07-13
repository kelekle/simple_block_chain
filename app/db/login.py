#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: login.py
@time: 2019/7/3 0:02'''

from db.dbaction import DBAction
import time

table_list = ["sale", "process", "transfer", "buyed"]


class Login(object):

    def __init__(self):
        self.db_action = DBAction()

    def check_login(self, id, password, phone_num=None):
        id_query = "select uid from users where uid = '" + str(id) + "'"
        pass_query = "select password from users where uid = '" + str(id) + "'"
        id_res = self.db_action.inquery(id_query)
        if id_res == -1:
            print("您输入的用户名不存在!")
            return False
        pass_res = self.db_action.inquery(pass_query)
        if pass_res['password'] == password:
            print("登陆成功!")
            return True
        else:
            print("密码错误!")
            return False

    def register(self, id, password, phone_num):
        id_query = "select uid from users where uid = " + id
        phone_query = "select phone_num from users where phone_num = '" + phone_num + "'"
        user_insert = "insert into users values(" + id + ", " + password + ", '" +\
                      phone_num + "', 0, 0, 0, 0, 0, 0" + ")"
        id_res = self.db_action.inquery(id_query)
        if id_res == 0:
            print("用户已注册!")
            return False, "该用户已注册!"
        else:
            phone_res = self.db_action.inquery(phone_query)
            if phone_res == 0:
                print("用户已注册!")
                return False, "该用户已注册!"
            else:
                insert_res = self.db_action.operate(user_insert)
                if insert_res != 0:
                    print("注册失败")
                    return False, "注册失败!"
                else:
                    print("注册成功")
                    return True, "注册成功!"

    def change_password(self, new_password, email):
        email_query = "select * from users where phone_num = '" + email + "'"
        email_res = self.db_action.inquery(email_query)
        if email_res == -1:
            print("该用户不存在!")
            return False
        else:
            update_query = "update users set password = " + new_password + " where phone_num = '" + email + "'"
            res = self.db_action.operate(update_query)
            if res != 0:
                print("更改失败")
                return False
            else:
                print("更改成功")
                return True

    # def change_password(self, old_password, new_password, phone_num):
    #     id_query = "select uid from users where uid = " + id
    #     pass_query = "select password from users where uid = " + id
    #     id_res = self.db_action.inquery(id_query)
    #     if id_res == 0:
    #         print("该用户名不存在!")
    #         return False
    #     update = "update users set password = " + new_password + "where uid = " + id
    #     pass_res = self.db_action.inquery(pass_query)
    #     if pass_res == old_password:
    #         update_res = self.db_action.operate(update)
    #         if update_res != 0:
    #             return False
    #         return True
    #     else:
    #         if phone_num != None:
    #             phone_query = "select phone_num from users where uid = " + id
    #             phone_res = self.db_action.inquery(phone_query)
    #             if phone_res == phone_num:
    #                 update_res = self.db_action.operate(update)
    #                 if update_res != 0:
    #                     return False
    #                 return True
    #         print("手机号错误!")
    #         return False

    def find_password(self, phone_num, new_password):
        id_query = "select uid from users where phone_num = " + phone_num
        id_res = self.db_action.inquery(id_query)
        if id_res == 0:
            print("该用户名不存在!")
            return False
        update_password = "update users set password  = " + new_password + " where phone_num = " + phone_num
        update_res = self.db_action.operate(update_password)
        if update_res != 0:
            print("执行失败!")
            return False
        else:
            return True

    def is_inserted(self, pid, cur_process):
        insert_query = "select * from " + table_list[cur_process - 1] + " where pid = '" + str(pid) + "'"
        res = self.db_action.inquery(insert_query)
        if res == -1:
            return False
        else:
            return True

    def push_product(self, uid, product_info, status):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        product_insert = "insert into sale values( "+ product_info['pid'] + " ,'" +  product_info['name'] + "', '" + time_str + "', '" + \
                         product_info['address'] + "', '" + product_info['performer'] + "', '" + \
                         product_info['contact'] + "', '" + product_info['info'] + "', '" + \
                         product_info['discribe'] + "', " + str(status) + ")"
        pi_res = self.db_action.operate(product_insert)
        if pi_res == 0:
            relation_insert = "insert into up_relation (uid, pid, step) values('" + str(uid) + "', '" + str(product_info['pid']) + "', " + "1" + ")"
            ri_res = self.db_action.operate(relation_insert)
        if pi_res != 0 or ri_res != 0:
            print("执行失败")
            return False
        return True

    def process_product(self, uid, pid, product_info, cur_process, status):
        if cur_process == 1:
            return False
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        product_insert = "insert into " + table_list[cur_process - 1] + " (pid, optime, address, performer, contact, " \
                         "discribe, status) values( '" + str(pid) + "', '" + time_str + "', '" + product_info['address'] \
                         + "', '" + product_info['performer'] + "', '" + product_info['contact'] + "', '" + \
                         product_info['discribe'] + "', '" + str(status) + "' )"
        pi_res = self.db_action.operate(product_insert)
        if pi_res == 0:
            relation_insert = "insert into up_relation  (uid, pid, step) values (" + str(uid) + ", " + str(pid) + \
                              ", '" + str(cur_process) + "' )"
            ri_res = self.db_action.operate(relation_insert)
        if pi_res != 0 or ri_res != 0:
            print("执行失败")
            return True
        return False

    def update_status(self, cur_process, status, pid):
        update_query = "update " + table_list[cur_process - 1] + " set status = " + str(status)\
                       + " where pid = " + str(pid)
        self.db_action.operate(update_query)

    def get_status(self, cur_process, pid):
        query = "select status from " + table_list[cur_process - 1] + " where pid = " + str(pid)
        res = self.db_action.inquery(query)
        return res

    def get_products(self, id):
        id_query = "select * from up_relation where uid = '" + str(id) + "'"
        res = self.db_action.data_inquiry_all(id_query)
        result = []
        completed_pid = []
        for item in res:
            if item['pid'] not in completed_pid:
                if item['step'] == 1:
                    temp_res = self.db_action.inquery("select status from sale where pid = " + str(item['pid']))
                    if temp_res['status'] != 2:
                        continue
                info_query = "select * from sale where pid = " + str(item['pid'])
                info_res = self.db_action.inquery(info_query)
                result.append(info_res)
                completed_pid.append(item['pid'])
        if result is not None:
            return result
        else:
            return None

    def get_user_nums(self):
        num_query = "select count(*) from users"
        res = self.db_action.inquery(num_query)
        return res['count(*)']

    def get_cur_step(self, uid, pid):
        id_query = "select * from up_relation where (uid = " + str(uid) + " and pid = " + str(pid)
        query_res = self.db_action.inquery(id_query)
        return query_res['step']

    def get_pre_list(self, uid):
        product_query = "select * from up_relation where uid = '" + str(uid) + "'"
        res = self.db_action.data_inquiry_all(product_query)
        if res is None:
            return None
        result = []
        completed_pid = []
        for item in res:
            if item['pid'] not in completed_pid:
                sale_query = "select * from sale where pid = " + str(item['pid'])
                sale_res = self.db_action.inquery(sale_query)
                result.append(sale_res)
                completed_pid.append(item['pid'])
        return result

    def get_sale_list(self):
        product_query = "select * from sale"
        res = self.db_action.data_inquiry_all(product_query)
        result = []
        for item in res:
            result.append(item)
        if result is None:
            return None
        else:
            return result

    def get_process_list(self):
        process_query = "select * from process"
        res = self.db_action.data_inquiry_all(process_query)
        result = []
        for item in res:
            sale_query = "select * from sale where pid = " + str(item['pid'])
            sale_res = self.db_action.inquery(sale_query)
            result.append(sale_res)
        if result is None:
            return None
        else:
            return result

    def get_transfer_list(self):
        transfer_query = "select * from transfer"
        res = self.db_action.data_inquiry_all(transfer_query)
        result = []
        for item in res:
            sale_query = "select * from sale where pid = " + str(item['pid'])
            sale_res = self.db_action.inquery(sale_query)
            result.append(sale_res)
        if result is None:
            return None
        else:
            return result

    def get_info(self, pid, cur_process):
        info_query = "select * from " + table_list[cur_process - 1] + " where pid = " + str(pid)
        res_info = self.db_action.inquery(info_query)
        if res_info == -1:
            return None
        else:
            return res_info

    def change_sale_info(self, pid, product_info):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        change_query = "update sale set name = '" + \
                        product_info['name'] + "',  birthday = '" + time_str + "', address = '" +\
                       product_info['address'] + "', performer = '" + product_info['performer'] + "', contact = '" +\
                       product_info['contact'] + "', info = '" + product_info['info'] + "', discribe = '" + \
                       product_info['discribe'] + "' " + "where pid = " + str(pid)
        self.db_action.operate(change_query)

    def change_info(self, pid, product_info, cur_process):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        change_query = "update " + table_list[cur_process - 1] + " set optime = '" + time_str + "', address = '" + \
                       product_info['address'] + "', performer = '" + product_info['performer'] + "', contact = '" + \
                       product_info['contact'] + "', discribe = '" + \
                       product_info['discribe'] + "' " + "where pid = " + str(pid)
        self.db_action.operate(change_query)

    def change_process_info(self, pid, product_info):
        self.change_info(pid, product_info, 2)

    def change_transfer_info(self, pid, product_info):
        self.change_info(pid, product_info, 3)

    def change_buy_info(self, pid, product_info):
        self.change_info(pid, product_info, 4)

    def delete(self, uid, pid, cur_process):
        delete_query = "delete from " + table_list[cur_process - 1] + " where pid = " + str(pid)
        self.db_action.operate(delete_query)
        delete_relation = "delete from up_relation where (pid = " + str(pid) + " and uid = " + str(uid) + ")"
        self.db_action.operate(delete_relation)

