#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from user import user_blue
from flask import render_template, flash, redirect, url_for, request
from user.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app import database


@user_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@user_blue.teardown_request
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@user_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('user.index'))  # 重定向到/user/index


@user_blue.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("user_index.html",
                           current_user=current_user)  #html的名字不能相同


@user_blue.route('/order', methods=['GET', 'POST'])
def order():
    return render_template("user_order.html", current_user=current_user)


#个人认为，“我的订单”页面不应该被别人看见


@user_blue.route('/publish', methods=['GET', 'POST'])
def publish():
    return render_template("user_publish.html", current_user=current_user)


#个人中心
@user_blue.route('/<opt_userid>/space', methods=['GET', 'POST'])
def space(opt_userid: int):  #opt_userid为目标用户ID
    if current_user.is_authenticated:
        return render_template('user_space.html')
    else:
        return redirect(url_for('index'))  # 重定向到/index


#个人信息管理
@user_blue.route('/<opt_userid>/user_info', methods=['GET', 'POST'])
def user_info(opt_userid: int):  #opt_userid为目标用户ID
    if current_user.is_authenticated:
        return render_template('user_info.html',
                               current_user=current_user,
                               opt_userid=opt_userid)
    else:
        return redirect(url_for('index'))  # 重定向到/index


#历史
@user_blue.route('/history', methods=['GET', 'POST'])
def history():
    if current_user.is_authenticated:
        return render_template('user_history.html')
    else:
        return redirect(url_for('index'))  # 重定向到/index


#收藏
@user_blue.route('/favor', methods=['GET', 'POST'])
def favor():
    if current_user.is_authenticated:
        return render_template('user_favor.html')
    else:
        return redirect(url_for('index'))  # 重定向到/index


@user_blue.route('/address', methods=['GET', 'POST'])
def address():
    if current_user.is_authenticated:
        return render_template('user_address.html')
    else:
        return redirect(url_for('index'))  # 重定向到/index
