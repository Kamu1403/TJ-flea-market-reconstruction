#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
###主要是注册登录管理

from app import app,database
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager
from user.models import User
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(student_number):
    try:
        user = User.get(User.student_number == student_number)  # 查
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
