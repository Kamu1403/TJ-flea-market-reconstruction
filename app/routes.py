#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from app import db as database
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.models import User
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from app import login


@app.before_request
def before_request():
    database.connect()
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.save()  # db.session.commit()


@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()


@app.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('index'))  # 重定向


@app.route('/index', methods=['GET', 'POST'])
# 这样，必须登录后才能访问首页了,会自动跳转至登录页
def index():
    if request.method == 'POST':
        return render_template("index.html")
    return render_template('index.html')
