#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
###主要是注册登录管理
from ast import keyword
import email
from app import app,database
from flask import render_template,flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import User#模型
from werkzeug.security import generate_password_hash
from user.models import User_state#枚举

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
def index():
    if request.method == 'POST':
        search_keyword = request.form.get('search')
        return redirect(url_for('search', keyword=search_keyword))
    #-------------配合前端搜索框的修改---------------
    # if request.method=='POST':
    #     search_keyword=request.form.get('key_word')  #输入框更名为key_word
    #     return redirect(url_for('search',keyword=search_keyword))      
    return render_template('index.html')


@app.route('/search/<keyword>', methods=['GET', 'POST'])
def search(keyword: str):  #keyword为你搜索的东西
    return render_template('search.html', keyword=keyword)

#-------------配合前端添加搜索结果页面---------------
#     return render_template('search_result.html',keyword=keyword) #搜索结果页面

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

        try:
            user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否时管理员        
        except:
            flash('无效的学号,请检查输入或注册')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        else:
            # 查到了，判断密码
            if not user.check_password(password):
                # 如果用户不存在或者密码不正确就会闪现这条信息
                flash('密码错误')
                # 然后重定向到登录页面
                return redirect(url_for('login'))
            if user.state==-1:
                #被封号了
                flash("您已被封号")
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
        is_admin=False
        if request.form.get('is_admin')=='on':
            is_admin=True
        state=User_state.Normal.value
        if is_admin:
            state=User_state.Admin.value

        try:
            user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否为管理员
            flash('该学号已被注册')
        except:
            User.create(id=user_id,username=user_id,state=state,
                        password_hash=generate_password_hash(password),
                        email=str(user_id)+"@tongji.edu.cn")
            return redirect(url_for('login'))

    return render_template('register.html')
