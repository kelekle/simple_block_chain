#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: form.py
@time: 2019/7/9 8:52'''

import re
from flask_wtf import *
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email


def is_id(form, field):
    uid = field.data
    ret = re.match('^\d{1,10}$', uid)
    if ret is None:
        raise ValidationError("must be 1 - 10 's digits!!!")


def is_phone_num(form, field):
    phone_num = field.data
    ret = re.match("^[1][345678][0-9]{9}$", phone_num)
    if ret is None:
        raise ValidationError("请输入正确的手机号!!!")

def is_email(form, field):
    email = field.data
    # ret = re.match("^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])$", email)
    ret = re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", email)
    if ret is None:
        return False
    else:
        return True

def email_val(form, filed):
    email = filed.data
    ret = re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", email)
    if ret is None:
        raise ValidationError("请输入正确的邮箱!!!")

def is_code(form, field):
    code = field.data
    ret = re.match("^\d{6}$")
    if ret is None:
        raise ValidationError("验证码格式错误!!!")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 10), is_id])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 12)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log  in')


class RegisterForm(FlaskForm):
    user_id = StringField('Username', validators=[DataRequired(), Length(1, 10), is_id])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 12)])
    email = StringField('email', validators=[DataRequired(), email_val])
    code = StringField('code', validators=[DataRequired(), Length(6, 6)])
    send_code = SubmitField('发送验证码')
    submit = SubmitField('Register')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email_val])
    code = StringField('code', validators=[DataRequired(), Length(6, 6)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 12)])
    send_code = SubmitField('发送验证码')
    submit = SubmitField('Reset')


class SaleForm(FlaskForm):
    pid = StringField('Product-ID', validators=[DataRequired(), Length(1, 10), is_id])
    name = StringField('Name', validators=[DataRequired()])
    info = StringField('Info', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    performer = StringField('Performer', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired(), is_phone_num])
    op_description = StringField('op_description')
    submit = SubmitField('保存')


class EditForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    performer = StringField('Performer', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired(), is_phone_num])
    op_description = StringField('op_description')
    submit = SubmitField('保存')
