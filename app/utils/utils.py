#!/usr/bin/env python
# encoding: utf-8
'''
@author: kle
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: utils.py
@time: 2019/7/4 23:21'''

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
import qrcode
from flask import request, redirect, url_for, current_app
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import datetime

smtp_host = "smtp.sina.com"
pop_host = "pop.sina.com"
port = 25
username = "ypb12345678910@sina.com"
password = "******"


class Utils(object):
    def __init__(self):
        pass

    def is_safe_url(self, target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

    def redirect_back(self, default='blog.index', **kwargs):
        for target in request.args.get('next'), request.referrer:
            if not target:
                continue
            if self.is_safe_url(target):
                return redirect(target)
        return redirect(url_for(default, **kwargs))

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']

    def gen_qrcode(file_name, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(file_name)

    def send_val_code(self, receiver, code):
        message = MIMEText("您的验证码是: " + str(code), 'plain', 'utf-8')
        message['from'] = Header(username)
        message['To'] = Header(receiver)
        message['Subject'] = Header('商品溯源系统验证邮件', 'utf-8')
        try:
            stmpObj = smtplib.SMTP(smtp_host, port)
            stmpObj.login(username, password)
            stmpObj.sendmail(username, receiver, message.as_string())
            print("发送邮件成功")
            return True
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件 ", e)
            return False


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
