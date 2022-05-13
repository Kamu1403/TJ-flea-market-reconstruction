#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from item import item_blue
from app import database
from item.models import Item, History, Favor
from datetime import date, datetime
from flask import make_response, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user

from user.models import User_state
import json

@item_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@item_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()


@item_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('item.index'))  # 重定向到/index


@item_blue.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('item_index.html')


@item_blue.route('/goods/<item_id>/', methods=['GET', 'POST'])
def goods_content(item_id:int):#goods_id/want_id
    if current_user.is_authenticated:
        try:
            last = History.get(History.item_id_id == item_id)
        except  Exception as e:
            last = History({"user_id":current_user.id,"item_id":item_id,"visit_time":datetime.utcnow()})
        else:
            last.visit_time = datetime.utcnow()
        finally:
            last.save()
    return render_template('item_content.html')

@item_blue.route('/want/<item_id>/', methods=['GET', 'POST'])
def want_content(item_id:int):#goods_id/want_id
    if current_user.is_authenticated:
        try:
            last = History.get(History.item_id_id == item_id)
        except  Exception as e:
            last = History({"user_id":current_user.id,"item_id":item_id,"visit_time":datetime.utcnow()})
        else:
            last.visit_time = datetime.utcnow()
        finally:
            last.save()
    return render_template('item_content.html')

@item_blue.route('/publish/goods/', methods=['GET', 'POST'])
def goods_publish():
    if request.method == "POST":
        if not current_user.is_authenticated:
            #总共是个报错
            flash("您还未登录,无法发布")
            return redirect(url_for("item.index"))
        data = request.form.to_dict()
        data['publish_id'] = current_user.id
        data['publish_time'] =str(date.today())
        data['lock_num'] = 0
        print(data)
        try:
            Item.insert(data).execute()
            pass
        except Exception as e:
            flash(f"发布商品时出现问题,具体为{str(e)}\n{repr(e)}\n")
            # return render_template('item_publish.html',name="goods")
        else:
            # return render_template('item_publish.html',name="goods")
            # 表示发布成功
            flash("发布商品成功")
        finally:
            return redirect(url_for("item.index"))
    return render_template('item_publish.html',name="goods")

@item_blue.route('/publish/want/', methods=['GET', 'POST'])
def want_publish():
    if request.method == "POST":
        if not current_user.is_authenticated:
            #总共是个报错
            flash("您还未登录,无法发布")
            return redirect(url_for("item.index"))
        data = request.form.to_dict()
        data['publish_id'] = current_user.id
        data['publish_time'] =str(date.today())
        data['lock_num'] = 0
        print(data)
        try:
            Item.insert(data).execute()
        except Exception as e:
            flash(f"发布悬赏时出现问题,具体为{str(e)}\n{repr(e)}\n")
            # return render_template('item_publish.html',name='want')
        else:
            flash("发布悬赏成功")
            # return render_template('item_publish.html',name='want')
            # 表示发布成功
        finally:
            return redirect(url_for("item.index"))
    return render_template('item_publish.html',name='want')
