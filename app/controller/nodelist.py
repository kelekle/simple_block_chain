#!/usr/bin/env python
# encoding: utf-8
'''
@author: kle
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: nodelist.py
@time: 2019/7/7 19:43'''

import zmq
import json
import threading
from queue import Queue
import sys
import time
sys.path.append('..')
from controller.publisher import Publisher
from db.login import Login
from utils.utils import *


# task to completed for one block
class Task(object):
    computed = False
    finished = False
    PROCESSING = False

    @staticmethod
    def new_block_signal(data):
        Task.PROCESSING = True
        while True:
            pub_write = Publisher(port=5002)
            pub_write.publish(json.dumps(data, cls=DateEncoder))
            time.sleep(10)
            if Task.computed:
                Task.computed = False
                break

    @staticmethod
    def send_new_block():
        data_dict = CompleteList.task_queue.get()
        login = Login()
        CompleteList.HALF_USER_NUM = login.get_user_nums() / 2
        while True:
            pub_write = Publisher(5004)
            pub_write.publish(json.dumps(data_dict['finished']))
            if Task.finished:
                print("dict:  ", data_dict)
                login.update_status(CompleteList.CUR_PROCESS, 2,
                                    str(data_dict['finished'][str(CompleteList.CUR_STEP)]['pid']))
                Utils.gen_qrcode("static/images/QRImage/" + str(data_dict['finished'][str(CompleteList.CUR_STEP)]['pid']) +
                                 "-" + CompleteList.CUR_STEP + ".jpg", data_dict['finished'])
                Task.finished = False
                Task.PROCESSING = False
                break
            time.sleep(10)


# waiting for at least half of all people received one block
class CompleteList(threading.Thread):

    HALF_USER_NUM = 0
    task_queue = Queue()
    user_completed_list = []
    CUR_PROCESS = 1
    CUR_STEP = "step1"

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def count_nums(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5001")
        num = 0
        while True:
            data = json.loads(socket.recv_json())
            if "ok" in data and data['uid'] not in self.user_completed_list:
                num += 1
                self.user_completed_list.append(data['uid'])
            print("5001 received and nums: ", num, " half nums: ", self.HALF_USER_NUM, "  data: ", data)
            if num > self.HALF_USER_NUM:
                Task.finished = True
                self.user_completed_list.clear()
                break
            socket.send_json(json.dumps({'ok_server': 'true'}))
        socket.close()

    def run(self):
        while True:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:5003")
            while True:
                print("task size", CompleteList.task_queue.qsize())
                data = socket.recv_json()
                data_dict = json.loads(data)
                if data_dict['finished'] is not None:
                    if self.task_queue.qsize() == 0:
                        print("5003 received computed finished: ", data)
                        Task.computed = True
                        self.task_queue.put(data_dict)
                        count_thread = threading.Thread(target=self.count_nums)
                        count_thread.start()
                        time.sleep(0.2)
                        Task.send_new_block()
                        break
                    else:
                        print("already have task")
                socket.send_json(json.dumps({'ok': 'true'}))
            socket.close()


# make a information interchange between client and this serever
class LoginList(threading.Thread):
    ChainList = []
    Chain_data = {}

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5005")
        all_list = []
        data_list = []
        user_completed_list = []
        while True:
            your_data = json.loads(socket.recv_json())
            socket.send_json("done")
            print("your data: ", your_data, "  ", data_list)
            if 'nothing' in your_data:
                continue
            else:
                uid = your_data['uid']
                del your_data['uid']
                if uid not in user_completed_list:
                    if your_data not in data_list:
                        data_list.append(your_data)
                        copy_data = your_data.copy()
                        copy_data['times'] = 1
                        all_list.append(copy_data)
                        print("no +1")
                    else:
                        print("+1")
                        all_list[data_list.index(your_data)]['times'] += 1
                user_completed_list.append(uid)
            all_list.sort(key=lambda x : x['times'], reverse=True)
            print("all_list: ", all_list)
            times = all_list[0]['times']
            print("times: ", times)
            print("my_half: ", CompleteList.HALF_USER_NUM)
            if times >= CompleteList.HALF_USER_NUM:
                del all_list[0]['times']
                publisher = Publisher(port=5006)
                publisher.publish(json.dumps(all_list[0]))
                LoginList.Chain_data = all_list[0]
                print(LoginList.Chain_data)
                data_list.clear()
                all_list.clear()
                user_completed_list.clear()
