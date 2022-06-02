#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from admin import admin_blue
from admin.models import Feedback
from app import database
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from user.models import User_state



@admin_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@admin_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()

@admin_blue.route('/user_check', methods=['GET', 'POST'])
def user_check():
    return render_template('user_check.html')
@admin_blue.route('/order_check', methods=['GET', 'POST'])
def order_check():
    return render_template('order_check.html')
@admin_blue.route('/feedback_show', methods=['GET', 'POST'])
def feedback_show():
    if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        return render_template('feedback_show.html')
    else:
        return render_template('404.html', error_code=401, message="您无权访问此页面")

@admin_blue.route("/feedback/<int:feedback_id>/",methods=["GET","POST"])
def feedback(feedback_id:int):
    if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        try:
            feedback = Feedback.get(Feedback.id == feedback_id)
        except Exception as e:
            return render_template("404.html", error_code=404, message="此反馈不存在")
        else:
            return render_template("feedback_content.html",feedback_id = feedback_id)
    else:
        return render_template('404.html', error_code=401, message="您无权访问此页面")
