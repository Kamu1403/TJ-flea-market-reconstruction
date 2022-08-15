#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from admin import admin_blue
from admin.models import Feedback, Feedback_state
from app import database
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from user.models import User_state
from functools import wraps


@admin_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@admin_blue.teardown_request
def teardown_request(exc):  # exc必须写上
    if not database.is_closed():
        database.close()


class AdminController:
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
                from user.models import User_state
                if current_user.is_authenticated and current_user.state == User_state.Admin.value:
                    return f(*args, **kwargs)
                else:
                    return authenticate()

            return decorated

        return auth_func

    @staticmethod
    @admin_blue.route('/user_check', methods=['GET', 'POST'])
    @requires_auth(show_err=401)
    def user_check():
        # if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        return render_template('user_check.html')
        # else:
        #     return render_template('404.html', error_code=401, message="您无权访问此页面")

    @staticmethod
    @admin_blue.route('/order_check', methods=['GET', 'POST'])
    @requires_auth(show_err=401)
    def order_check():
        # if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        return render_template('order_check.html')
        # else:
        #     return render_template('404.html', error_code=401, message="您无权访问此页面")

    @staticmethod
    @admin_blue.route('/feedback_show', methods=['GET', 'POST'])
    @requires_auth(show_err=401)
    def feedback_show():
        # if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        return render_template('feedback_show.html')
        # else:
        #     return render_template('404.html', error_code=401, message="您无权访问此页面")

    @staticmethod
    @admin_blue.route("/feedback/<int:feedback_id>/", methods=["GET", "POST"])
    @requires_auth(show_err=401)
    def feedback(feedback_id: int):
        # if current_user.is_authenticated and current_user.state == User_state.Admin.value:
        try:
            feedback = Feedback.get(Feedback.id == feedback_id)
        except Exception as e:
            return render_template("404.html",
                                   error_code=404,
                                   message="此反馈不存在")
        else:
            if feedback.state == Feedback_state.Unread.value:
                feedback.state = Feedback_state.Read.value
                feedback.save()
            return render_template("feedback_content.html",
                                   feedback_id=feedback_id)
        # else:
        #     return render_template('404.html', error_code=401, message="您无权访问此页面")
