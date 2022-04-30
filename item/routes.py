#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from item import item_blue
from app import database
from item.models import Goods, Want, HistoryGoods, HistoryWant, FavorGoods, FavorWant
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request




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
    return 'Hello World!'

@item_blue.route('/goods/<item_id>/', methods=['GET', 'POST'])
def goods_content(item_id:int):#goods_id/want_id
    print(item_id)
    return render_template('item_content.html')

@item_blue.route('/want/<item_id>/', methods=['GET', 'POST'])
def want_content(item_id:int):#goods_id/want_id
    print(item_id)
    return render_template('item_content.html')

@item_blue.route('/publish/goods/', methods=['GET', 'POST'])
def goods_publish():
    return render_template('item_publish.html')

@item_blue.route('/publish/want/', methods=['GET', 'POST'])
def want_publish():
    return render_template('item_publish.html')
