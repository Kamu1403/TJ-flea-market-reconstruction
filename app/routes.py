#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
###主要是注册登录管理
from app import app, database
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import User  #模型
from werkzeug.security import generate_password_hash

from flask_socketio import SocketIO, emit

from user.models import User_state  #枚举

from flask_login import LoginManager

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):  #login时传入
    try:
        user = User.get(User.id == id)  # 查
    except:
        user = None
    return user


@app.before_request
def before_request():
    if database.is_closed():
        database.connect()


@app.teardown_request
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def rootindex():
    return redirect(url_for('index'))  # 重定向


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_keyword = request.form.get('search')
        if len(search_keyword) > 0:
            return redirect(url_for('search', keyword=search_keyword))
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('index.html')


@app.route('/search/<keyword>', methods=['GET', 'POST'])
def search(keyword: str):  #keyword为你搜索的东西
    return render_template('search.html', keyword=keyword)


@app.route('/register', methods=['GET'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('verify_login.html')


@app.route('/forget', methods=['GET'])
def forget():
    return render_template('verify_login.html', forget=True)


@app.route('/login', methods=['GET'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('password_login.html')