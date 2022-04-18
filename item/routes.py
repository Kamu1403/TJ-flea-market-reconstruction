#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from item import item_blue
from app import database
from item.models import Goods, Want, HistoryGoods, HistoryWant, FavorGoods, FavorWant
from datetime import datetime




@item_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@item_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()


@item_blue.route("/")
def root_index():
    return redirect(url_for('item.index'))  # 重定向到/index


@item_blue.route('/index')
def index():
    return 'Hello World!'
    #if request.method == 'POST':
    #    return render_template("index.html")
    #return render_template('index.html')
