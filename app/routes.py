#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
###主要是注册登录管理

import os
import json
from datetime import datetime
from app import app, database
from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from user.models import User  # 模型
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO, emit
from user.models import User_state  # 枚举
from flask_login import LoginManager
from functools import wraps

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):  # login时传入
    try:
        user = User.get(User.id == id)  # 查
    except:
        user = None
    return user


@app.before_request
def before_request():
    if database.is_closed():
        database.connect()


@app.before_request
def state_check():
    if current_user.is_authenticated:
        if current_user.state == User_state.Under_ban.value:
            logout_user()


# @app.before_request
# def request_log():
#     with open(os.path.join(app.static_folder,"test.json"),"a+") as f:
#         d = dict()
#         #d["header"] = request.headers.__dict__
#         d["ip"] = request.remote_addr
#         d["url"] = request.url
#         d["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
#         if current_user.is_authenticated:
#             d["user_id"] = current_user.id
#         json.dump(d,f)
#         f.write(",\n")


@app.after_request
def log(response: Response) -> Response:
    with open(os.path.join(app.static_folder, "history.log"), "a+") as f:
        d = dict()
        d["url"] = request.url
        d["ip"] = request.remote_addr
        d["request_headers"] = list(request.headers)
        # d["header"] = request.headers.__dict__
        d["status"] = response.status_code
        d["response_headers"] = list(response.headers)
        d["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
        if current_user.is_authenticated:
            d["user_id"] = current_user.id
        # json.dump(d, f, ensure_ascii=False)
        # f.write('\n')
    return response


@app.teardown_request
def teardown_request(exc):  # exc必须写上
    if not database.is_closed():
        database.close()


class AppController:
    @staticmethod
    def ready_auth(f):
        def ready():
            return redirect(url_for('user.index'))

        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if current_user.is_authenticated:
                return ready()
            else:
                return f(*args, **kwargs)

        return decorated

    @staticmethod
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @staticmethod
    @app.route("/")
    def rootindex():
        return redirect(url_for('index'))  # 重定向

    @staticmethod
    @app.route('/index', methods=['GET', 'POST'])
    @ready_auth
    def index():
        if request.method == 'POST':
            search_keyword = request.form.get('search')
            if len(search_keyword) > 0:
                return redirect(url_for('search', keyword=search_keyword))
        # if current_user.is_authenticated:
        #     return redirect(url_for('user.index'))
        return render_template('index.html')

    @staticmethod
    @app.route('/search', methods=['GET', 'POST'])
    def search():  # keyword为你搜索的东西
        data = dict()
        try:
            data["keyword"] = request.args["keyword"]
            data["search_type"] = request.args["search_type"]
        except:
            return render_template('404.html', message="格式错误", error_code=400)
        return render_template('search.html', **data)

    @staticmethod
    @app.route('/register', methods=['GET'])
    @ready_auth
    def register():
        # # 判断当前用户是否验证，如果通过的话返回首页
        # if current_user.is_authenticated:
        #     return redirect(url_for('user.index'))
        return render_template('verify_login.html')

    @staticmethod
    @app.route('/forget', methods=['GET'])
    def forget():
        return render_template('verify_login.html', forget=True)

    @staticmethod
    @app.route('/set_password', methods=['GET'])
    def set_password():
        return render_template('verify_login.html', set_password=True)

    @staticmethod
    @app.route('/login', methods=['GET'])
    @ready_auth
    def login():
        # # 判断当前用户是否验证，如果通过的话返回首页
        # if current_user.is_authenticated:
        #     return redirect(url_for('user.index'))
        return render_template('password_login.html')

    @staticmethod
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", message=error, error_code=404)
