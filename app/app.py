#!/usr/bin/env python
# encoding: utf-8
'''
@author: yangpb
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 1524183302@qq.com
@file: app.py
@time: 2019/7/3 14:45'''

import os
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, flash, redirect, url_for, Markup, request
from flask_wtf.csrf import CSRFError
from db.login import *
from model.User import *
import random
from utils.utils import *
from controller.nodelist import *
from controller.publisher import *
from form import *


NEW = 0
PROCESSING = 1
COMPLETED = 2

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    print("load: ", user_id)
    return User(user_id)


@app.route("/login", methods=['GET', 'POST'])
@app.route("/login.html", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        login = Login()
        uid = form.username.data
        password = form.password.data
        result = login.check_login(uid, password, phone_num=None)
        remember_me = False
        if form.remember:
            remember_me = True
        if result:
            user = User(uid)
            user.set_password(password)
            login_user(user=user, remember=remember_me)
            current_user.is_first_login = True
            current_user.id = uid
            if current_user.is_first_login:
                flash("欢迎使用商品溯源系统!!!")
                current_user.is_first_login = False
            return render_template('home.html', user_id=uid)
        else:
            flash('Invalid username or password.', 'warning')
    return render_template('index.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("登出成功!")
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.send_code.data:
        if is_email(form, form.email):
            utils = Utils()
            current_user.ran = random.randint(100000, 999999)
            if utils.send_val_code(form.email.data, current_user.ran):
                flash("验证码已发送", "info")
    if form.submit.data and form.validate_on_submit():
        uid = form.user_id.data
        password = form.password.data
        email = form.email.data
        print(form.code.data , "  ", current_user.ran)
        if str(form.code.data) != str(current_user.ran):
            flash("验证码错误!!!", "warning")
        else:
            login = Login()
            result = login.register(uid, password, email)
            if result is not None:
                flash("注册成功!", "info")
                CompleteList.HALF_USER_NUM = login.get_user_nums() / 2
                return redirect(url_for('register'))
    return render_template('register.html', form=form)


@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.send_code.data:
        utils = Utils()
        current_user.ran = random.randint(100000, 999999)
        if utils.send_val_code(form.email.data, current_user.ran):
            flash("验证码已发送", "info")
    if form.submit.data and form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        if str(form.code.data) != str(current_user.ran):
            flash("验证码错误!!!", "warning")
        else:
            login = Login()
            result = login.change_password(password, email)
            if result is not None:
                flash("更改密码成功!", "info")
                return redirect(url_for('forgot'))
    return render_template('forgot.html', form=form)


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')


@app.route('/sale_thing')
@login_required
def sale_thing():
    print("cur id:", current_user.id, "  ", current_user.username)
    login = Login()
    items = login.get_pre_list(current_user.id)
    return render_template('sale_thing.html', items=items)


@app.route('/process')
@login_required
def process_product():
    login = Login()
    items = login.get_sale_list()
    return render_template("/process.html", login=login, items=items)


@app.route('/transfer')
@login_required
def transfer_product():
    login = Login()
    items = login.get_process_list()
    return render_template("/transfer.html", login=login, items=items)


@app.route('/buy_thing')
@login_required
def buy_product():
    login = Login()
    items = login.get_transfer_list()
    return render_template("/buy_thing.html", login=login, items=items)


@app.route("/edit_info_sale_fir", methods=['GET', 'POST'])
@login_required
def edit_info_sale_fir():
    form = SaleForm()
    login = Login()
    if form.validate_on_submit():
        product_info = {}
        product_info['pid'] = form.pid.data
        product_info['name'] = form.name.data
        product_info['contact'] = form.contact.data
        product_info['address'] = form.address.data
        product_info['info'] = form.info.data
        product_info['discribe'] = form.op_description.data
        product_info['performer'] = form.performer.data
        if login.is_inserted(product_info['pid'], 1):
            flash("商品id已存在")
            print("商品id已存在")
            return redirect('/sale_thing')
        elif login.push_product(current_user.id, product_info, NEW):
            print("保存成功")
            return redirect('/sale_thing')
        else:
            print("保存失败")
    return render_template('edit_info_sale.html', info=None, inserted=False, form=form)


@app.route("/edit_info_sale/<id>", methods=['GET', 'POST'])
@login_required
def edit_info_sale(id):
    form = SaleForm()
    login = Login()
    inserted = login.is_inserted(id, 1)
    if inserted:
        info = login.get_info(id, cur_process=1)
    else:
        return redirect('/sale_thing')
    if form.validate_on_submit():
        product_info = {}
        product_info['pid'] = form.pid.data
        product_info['name'] = form.name.data
        product_info['contact'] = form.contact.data
        product_info['address'] = form.address.data
        product_info['info'] = form.info.data
        product_info['discribe'] = form.op_description.data
        product_info['performer'] = form.performer.data
        if login.is_inserted(product_info['pid'], 1):
            login.change_sale_info(product_info['pid'], product_info)
            print("保存成功")
            return redirect('/sale_thing')
        elif login.push_product(current_user.id, product_info, NEW):
            print("保存成功")
            return redirect('/sale_thing')
        else:
            print("保存失败")
    return render_template('edit_info_sale.html', info=info, inserted=inserted, form=form)


@app.route('/edit_info_process/<id>', methods=['GET', 'POST'])
@login_required
def edit_info_process(id):
    form = EditForm()
    login = Login()
    inserted = login.is_inserted(id, 2)
    info = None
    if inserted:
        info = login.get_info(id, cur_process=2)
    if form.validate_on_submit():
        product_info = {}
        product_info['contact'] = form.contact.data
        product_info['address'] = form.address.data
        product_info['discribe'] = form.op_description.data
        product_info['performer'] = form.performer.data
        if login.is_inserted(id, 2):
            login.change_process_info(id, process_product)
        else:
            login.process_product(current_user.id, id, product_info=product_info, cur_process=2, status=NEW)
        flash("已保存!")
        return redirect('/process')
    return render_template('edit_info.html', type=2, info=info, inserted=inserted, form=form)


@app.route('/edit_info_transfer/<id>', methods=['GET', 'POST'])
@login_required
def edit_info_transfer(id):
    form = EditForm()
    login = Login()
    inserted = login.is_inserted(id, 3)
    info = None
    if inserted:
        info = login.get_info(id, cur_process=3)
    if form.validate_on_submit():
        login = Login()
        product_info = {}
        product_info['contact'] = form.contact.data
        product_info['address'] = form.address.data
        product_info['discribe'] = form.op_description.data
        product_info['performer'] = form.performer.data
        if login.is_inserted(id, 3):
            login.change_transfer_info(id, product_info)
        else:
            login.process_product(current_user.id, id, product_info=product_info, cur_process=3, status=NEW)
        flash("已保存!")
        return redirect('/transfer')
    return render_template('edit_info.html', type=3, info=info, inserted=inserted, form=form)


@app.route('/edit_info_buy/<id>', methods=['GET', 'POST'])
@login_required
def edit_info_buy(id):
    form = EditForm()
    login = Login()
    inserted = login.is_inserted(id, 4)
    info = None
    if inserted:
        info = login.get_info(id, cur_process=4)
    if form.validate_on_submit():
        product_info = {}
        product_info['contact'] = form.contact.data
        product_info['address'] = form.address.data
        product_info['discribe'] = form.op_description.data
        product_info['performer'] = form.performer.data
        if inserted:
            login.change_buy_info(id, product_info)
        else:
            login.process_product(current_user.id, id, product_info=product_info, cur_process=4, status=NEW)
        flash("已保存!")
        return redirect('/buy_thing')
    return render_template('edit_info.html', type=4, info=info, inserted=inserted, form=form)


@app.route('/join_sale/<id>')
@login_required
def join_sale(id):
    if not Task.PROCESSING:
        login = Login()
        login.update_status(1, PROCESSING, id)
        CompleteList.CUR_PROCESS = 1
        CompleteList.CUR_STEP = "step1"
        block_obj = login.get_info(id, 1)
        block_obj['hash_pre'] = '0'
        block = {'step1': block_obj}
        Task.new_block_signal(block)
    return redirect('/sale_thing')


@app.route('/join_process/<id>')
@login_required
def join_process(id):
    if not Task.PROCESSING:
        login = Login()
        login.update_status(2, PROCESSING, id)
        CompleteList.CUR_PROCESS = 2
        CompleteList.CUR_STEP = "step2"
        block_obj = login.get_info(id, 2)
        block_obj['hash_pre'] = LoginList.Chain_data[str(id)]['step1']['hash_cur']
        block = {'step2': block_obj}
        Task.new_block_signal(block)
    return redirect('/process')


@app.route('/join_transfer/<id>')
@login_required
def join_transfer(id):
    if not Task.PROCESSING:
        login = Login()
        login.update_status(3, PROCESSING, id)
        CompleteList.CUR_PROCESS = 3
        CompleteList.CUR_STEP = "step3"
        block_obj = login.get_info(id, 3)
        print("chain ", LoginList.Chain_data)
        block_obj['hash_pre'] = LoginList.Chain_data[str(id)]['step2']['hash_cur']
        block = {'step3': block_obj}
        Task.new_block_signal(block)
    return redirect('/transfer')


@app.route('/join_buy/<id>')
@login_required
def join_buy(id):
    if not Task.PROCESSING:
        login = Login()
        login.update_status(4, PROCESSING, id)
        CompleteList.CUR_PROCESS = 4
        CompleteList.CUR_STEP = "step4"
        block_obj = login.get_info(id, 4)
        block_obj['hash_pre'] = LoginList.Chain_data[str(id)]['step3']['hash_cur']
        block = {'step4': block_obj}
        Task.new_block_signal(block)
    return redirect('/buy_thing')


@app.route('/delete_sale/<id>')
@login_required
def delete_sale(id):
    login = Login()
    login.delete(uid=current_user.id, pid=id, cur_process=1)
    return redirect('/sale_thing')


@app.route('/delete_process/<id>')
@login_required
def delete_process(id):
    login = Login()
    login.delete(current_user.id, id, 2)
    return redirect('/process')


@app.route('/delete_transfer/<id>')
@login_required
def delete_transfer(id):
    login = Login()
    login.delete(current_user.id, id, 3)
    return redirect('/transfer')


@app.route('/delete_buy/<id>')
@login_required
def delete_buy(id):
    login = Login()
    login.delete(current_user.id, id, 4)
    return redirect('/buy_thing')


@app.route('/my_products')
@login_required
def my_products():
    login = Login()
    items = login.get_products(current_user.id)
    return render_template('my_products.html', items=items)


@app.route("/block_cards/<id>")
@login_required
def block_cards(id):
    image_list = []
    for i in range(1, 5):
        if os.path.exists("./static/images/QRImage/" + str(id) + "-step" + str(i) + ".jpg"):
            image_list.append("../static/images/QRImage/" + str(id) + "-step" + str(i) + ".jpg")
    print(image_list)
    return render_template('block_cards.html', image_list=image_list)


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


# 400 error handler
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/400.html', description=e.description), 400
