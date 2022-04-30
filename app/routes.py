#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
###主要是注册登录管理
import email
from app import app,database
from flask import render_template,flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import User
from werkzeug.security import generate_password_hash

from flask_login import LoginManager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):#login时传入
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
def teardown_request(exc):#exc必须写上
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
# 这样，必须登录后才能访问首页了,会自动跳转至登录页
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    if request.method == 'POST':
        user_id=request.form.get('user_id')
        password=request.form.get('password')
        remember_me=False
        if request.form.get('remember_me')=='on':
            remember_me=True
        print(user_id,password,remember_me)

        try:
            user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否时管理员        
        except:
            print('无效的学号,请检查输入或注册')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
            
        # 查到了，判断密码
        if not user.check_password(password):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            print('密码错误')
            # 然后重定向到登录页面
            return redirect(url_for('login'))

        # 记住登录状态，同时维护current_user
        login_user(user, remember=remember_me)
        return redirect(url_for('user.index'))

    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    if request.method == 'POST':
        user_id=request.form.get('user_id')
        password=request.form.get('password')
        print(user_id,password)

        try:
            user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否为管理员
            print('该学号已被注册')
        except:
            print("create user")
            User.create(id=user_id,username=user_id,password_hash=generate_password_hash(password),email=str(user_id)+"@tongji.edu.cn")

            return redirect(url_for('login'))

    return render_template('register.html')
