#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from item import item_blue
from app import database
from item.models import Goods, Want, HistoryGoods, HistoryWant, FavorGoods, FavorWant
from datetime import datetime
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
    try:
        it = Goods.get(Goods.id==item_id)
    except Exception as e:
        it = None
    if it is None:
        #报错
        return redirect(url_for("item.index"))
    if not current_user.is_authenticated:
        isAdmin = False
        isPub = False
    else:
        isAdmin = (current_user.state == User_state.Admin.value)
        isPub =  it.publisher_id.id == current_user.id
    if not isAdmin and not isPub:
        pass
    elif isPub:
        pass
    else:
        pass
    return render_template('item_content.html')

@item_blue.route('/want/<item_id>/', methods=['GET', 'POST'])
def want_content(item_id:int):#goods_id/want_id
    try:
        it = Want.get(Want.id==item_id)
    except Exception as e:
        it = None
    if it is None:
        #报错
        return redirect(url_for("item.index"))
    if not current_user.is_authenticated:
        isAdmin = False
        isPub = False
    else:
        isAdmin = (current_user.state == User_state.Admin.value)
        isPub =  (it.publisher_id.id == current_user.id)
    if not isAdmin and not isPub:
        pass
    elif isPub:
        pass
    else:
        pass
    return render_template('item_content.html')

@item_blue.route('/publish/goods/', methods=['GET', 'POST'])
def goods_publish():
    if request.method == "POST":
        if not current_user.is_authenticated:
            #总共是个报错
            flash("您还未登录,无法发布")
            return redirect(url_for("item.index"))

        try:
            data = request.form.to_dict()
            data['publish_id'] = current_user.id
            data['publish_time'] =str(datetime.today())
            data['lock_num'] = 0
            print(data)
            # Goods.insert(data).execute()
            pass
        except Exception as e:
            pass
            # return render_template('item_publish.html',name="goods")
        else:
            pass
            # return render_template('item_publish.html',name="goods")
            # 表示发布成功
            #return redirect(url_for("item.index"))
    return render_template('item_publish.html',name="goods")

@item_blue.route('/publish/want/', methods=['GET', 'POST'])
def want_publish():
    if request.method == "POST":
        if not current_user.is_authenticated:
            #总共是个报错
            flash("您还未登录,无法发布")
            return redirect(url_for("item.index"))

        try:
            data = request.form.to_dict()
            data['publish_id'] = current_user.id
            data['publish_time'] =str(datetime.today())
            data['lock_num'] = 0
            print(data)
            # Want.insert(data).execute()
            pass
        except Exception as e:
            pass
            # return render_template('item_publish.html',name='want')
        else:
            pass
            # return render_template('item_publish.html',name='want')
            # 表示发布成功
            #return redirect(url_for("item.index"))
    return render_template('item_publish.html',name='want')
