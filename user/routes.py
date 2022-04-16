#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from user import user_blue
from flask import render_template, flash, redirect, url_for, request
from user.models import User
from flask_login import current_user, login_user, logout_user, login_required

from flask_login import LoginManager
from app import database

login = LoginManager(user_blue)


@user_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@user_blue.teardown_request
def teardown_request():
    if not database.is_closed():
        database.close()


@user_blue.route("/")
def root_index():
    return 'Hello World!'
    #return redirect(url_for('.index'))  # 重定向到/index


@user_blue.route('/index')
def index():
    return 'Hello World!'
    #if request.method == 'POST':
    #    return render_template("index.html")
    #return render_template('index.html')
