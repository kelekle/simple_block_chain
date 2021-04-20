#!/usr/bin/env python
# encoding: utf-8
'''
@author: kle
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: publisher.py
@time: 2019/7/7 19:47'''

import zmq
import time


class Publisher(object):

    def __init__(self, port):
        self.port = port

    def publish(self, data):
        endpoint = "tcp://*:" + str(self.port)
        context = zmq.Context()
        server = context.socket(zmq.PUB)
        server.bind(endpoint)
        time.sleep(1)
        # server.setsockopt(zmq.LENGER, "server")
        server.send_json(data)
        print(str(self.port) + " pub ", data)
        server.close()
