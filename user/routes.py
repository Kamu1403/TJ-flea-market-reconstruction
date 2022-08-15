#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from user import user_blue
from flask import render_template, flash, redirect, url_for, request
from user.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app import database
from functools import wraps


@user_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@user_blue.teardown_request
def teardown_request(exc):  # exc必须写上
    if not database.is_closed():
        database.close()


class UserController:
    @staticmethod
    def requires_auth(show_err=0):
        def auth_func(f):
            def authenticate():
                if show_err == 0:
                    return redirect(url_for('login'))
                elif show_err == 401:
                    return render_template('404.html', error_code=401, message="请先登录")
                elif show_err == 404:
                    return render_template("404.html", error_code=404, message="此反馈不存在")
                else:
                    raise Exception("unexpected requires_auth param")

            @wraps(f)
            def decorated(*args, **kwargs):
                from flask_login import current_user
                if current_user.is_authenticated:
                    return f(*args, **kwargs)
                else:
                    return authenticate()

            return decorated

        return auth_func

    @staticmethod
    @user_blue.route("/", methods=['GET', 'POST'])
    def root_index():
        return redirect(url_for('user.index'))  # 重定向到/user/index

    @staticmethod
    @user_blue.route('/index', methods=['GET', 'POST'])
    @requires_auth()
    def index():
        # if current_user.is_authenticated:
        return render_template("user_index.html", current_user=current_user)  # html的名字不能相同
        # else:
        #     return redirect(url_for('login'))

    @staticmethod
    @user_blue.route('/publish', methods=['GET', 'POST'])
    @requires_auth()
    def publish():
        # if current_user.is_authenticated:
        return render_template("user_publish.html", current_user=current_user)
        # else:
        #     return redirect(url_for('login'))

    # 个人中心
    @staticmethod
    @user_blue.route('/space', methods=['GET', 'POST'])
    def space():
        return redirect(url_for('user.order'))
        if current_user.is_authenticated:
            return render_template('user_space.html', current_user=current_user)
        else:
            return redirect(url_for('login'))

    # 个人信息管理
    @staticmethod
    @user_blue.route('/<opt_userid>/user_info', methods=['GET', 'POST'])
    @requires_auth(show_err=401)
    def user_info(opt_userid: int):  # opt_userid为目标用户ID
        # if current_user.is_authenticated:
        try:
            user = User.get(User.id == opt_userid)
        except:
            return render_template('404.html', message="找不到该用户")
        return render_template('user_info.html',
                               current_user=current_user,
                               opt_userid=int(opt_userid))
        # else:
        #     return render_template('404.html', error_code=401, message="请先登录")

    @staticmethod
    @user_blue.route('/order', methods=['GET', 'POST'])
    def order():
        return render_template("user_order.html", current_user=current_user)

    # 个人认为，“我的订单”页面不应该被别人看见

    # 历史
    @staticmethod
    @user_blue.route('/history', methods=['GET', 'POST'])
    @requires_auth()
    def history():
        # if current_user.is_authenticated:
        return render_template('user_history.html')

    # else:
    #     return redirect(url_for('login'))

    # 收藏
    @staticmethod
    @user_blue.route('/favor', methods=['GET', 'POST'])
    @requires_auth()
    def favor():
        # if current_user.is_authenticated:
        return render_template('user_favor.html')

    # else:
    #     return redirect(url_for('login'))

    @staticmethod
    @user_blue.route('/address', methods=['GET', 'POST'])
    @requires_auth()
    def address():
        # if current_user.is_authenticated:
        return render_template('user_address.html')

    # else:
    #     return redirect(url_for('login'))

    @staticmethod
    @user_blue.route("/feedback", methods=["GET", "POST"])
    @requires_auth()
    def feedback():
        # if current_user.is_authenticated:
        return render_template('user_feedback.html')
    # else:
    #     return redirect(url_for('login'))
