#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: subscriber.py
@time: 2019/7/4 9:22'''

import threading
import zmq
import time
import json
import sys
import os
sys.path.append("..")
# from controller.block_chain import *


from hashlib import sha256
import json
import time


class Block(object):

    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        # self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        # A function that return the hash of the block contents.
        block_string = str(self.transactions) + str(self.nonce)
        # block_string = json.dumps(self._dict_, sort_keys = True)
        return str(sha256(block_string.encode()).hexdigest())


class MessageThread(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.endpoint = "tcp://127.0.0.1:5002"

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        context = zmq.Context()
        client = context.socket(zmq.SUB)
        client.connect(self.endpoint)
        client.setsockopt(zmq.SUBSCRIBE, b'')  # Terminate early
        while True:
            print("5002 waiting...")
            rep = client.recv_json()
            reply = json.loads(rep)
            print("5002 received: ", reply)
            block = Block(reply, previous_hash=0)
            hash_result, noce = self.proof_of_work(block=block)
            for key in reply.keys():
                reply[key]['noce'] = str(noce)
                reply[key]['hash_cur'] = str(hash_result)
            MessageThread.send_finish_status(reply)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('O' * 5):
            block.nonce += 1
            computed_hash = block.compute_hash()
            # print(computed_hash)
            if computed_hash.startswith('0' * 5):
                break
        print(' 最终结果:{}, 随机数:{}'.format(computed_hash, block.nonce))
        return computed_hash, block.nonce

    @staticmethod
    def send_finish_status(block_object):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:5003")
        block_dict = {}
        block_dict['finished'] = block_object
        block_dict['uid'] = LoginThread.uid
        block_string = json.dumps(block_dict)
        print("5003 send: ", block_string)
        socket.send_json(json.dumps(block_dict))
        socket.recv_string()
        socket.close()


class Client(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.endpoint = "tcp://127.0.0.1:5004"

    def run(self):
        context = zmq.Context()
        client = context.socket(zmq.SUB)
        client.connect(self.endpoint)
        client.setsockopt(zmq.SUBSCRIBE, b'')
        while True:
            data = client.recv_json()
            reply = json.loads(data)
            print("5004 received", reply)
            for key in reply.keys():
                load_data = {}
                if os.path.exists('.\\data\\block\\pid-' + str(reply[key]['pid']) + '.txt'):
                    with open('.\\data\\block\\pid-' + str(reply[key]['pid']) + '.txt', 'r', encoding='utf-8') as f:
                        load_data = json.load(f)
                    if key in load_data:
                        continue
                    else:
                        load_data[key] = reply[key]
                        print("write data: ", load_data[key])
                        with open('.\\data\\block\\pid-' + str(reply[key]['pid']) + '.txt', 'w', encoding="utf-8") as f:
                            f.write(json.dumps(load_data, indent=2, ensure_ascii=False))
                else:
                    load_data[key] = reply[key]
                    with open('.\\data\\block\\pid-' + str(reply[key]['pid']) + '.txt', 'w', encoding="utf-8") as f:
                        f.write(json.dumps(load_data, indent=2, ensure_ascii=False))
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://127.0.0.1:5001")
            block_dict = {'ok': 'true', 'uid': LoginThread.uid}
            block_string = json.dumps(block_dict)
            print("5003 send: ", block_string)
            socket.send_json(json.dumps(block_dict))
            socket.recv_string()
            socket.close()


class LoginThread(threading.Thread):
    uid = ""

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.endpoint = "tcp://127.0.0.1:5006"

    def login(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:5005")
        while True:
            data_dict = {}
            for filename in os.listdir(os.getcwd() + "\\data\\block"):
                with open(".\\data\\block\\" + filename, 'r', encoding='utf-8') as f:
                    load_data = json.load(f)
                for key in load_data.keys():
                    data_dict[load_data[key]['pid']] = load_data
            if data_dict:
                data_dict['uid'] = self.uid
                socket.send_json(json.dumps(data_dict))
            else:
                socket.send_json(json.dumps({'nothing': "true"}))
            rec = socket.recv_json()
            print("my received: ", rec)
            time.sleep(60)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        context = zmq.Context()
        client = context.socket(zmq.SUB)
        client.connect(self.endpoint)
        client.setsockopt(zmq.SUBSCRIBE, b'')  # Terminate early
        while True:
            rep = client.recv_json()
            reply = json.loads(rep)
            print("5006 received: ", reply)
            for key in reply.keys():
                with open('.\\data\\block\\pid-' + key + '.txt', 'w', encoding="utf-8") as f:
                    f.write(json.dumps(reply[key], indent=2, ensure_ascii=False))
        client.close()


if __name__ == "__main__":
    login = LoginThread(1, "Thread-1", 1)
    LoginThread.uid = input("your uid")
    login_thread = threading.Thread(target=login.login)
    login_thread.start()
    login.start()
    handler2 = MessageThread(3, "Thread-3", 1)
    handler2.start()
    handler3 = Client(4, "Thread-4", 1)
    handler3.start()
