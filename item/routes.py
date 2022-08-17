#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from email import message
from http.client import responses
from urllib import response
from item import item_blue
from app import database
from item.models import Item, History, Favor, Item_type, Item_state
from datetime import date, datetime
from flask import make_response, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user

from user.models import User_state
import json
from functools import wraps


@item_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@item_blue.teardown_request
def teardown_request(exc):  # exc必须写上
    if not database.is_closed():
        database.close()


class ItemController:
    @staticmethod
    def auth_func(f):
        def authenticate():
            return render_template('404.html', message="请先登录")

        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if current_user.is_authenticated:
                return f(*args, **kwargs)
            else:
                return authenticate()

        return decorated

    @staticmethod
    @item_blue.route('/content/<item_id>/', methods=['GET'])
    def content(item_id: int):  # goods_id/want_id
        try:
            item = Item.get(Item.id == item_id)
        except:
            return render_template('404.html', error_code=404, message="该商品不存在")
        else:
            if not current_user.is_authenticated:
                is_admin = False
                is_pub = False
            else:
                is_admin = (current_user.state == User_state.Admin.value)
                is_pub = (item.user_id.id == current_user.id)
                if item.state != Item_state.Sale.value and not is_admin and not is_pub:
                    return render_template('404.html', error_code=401, message="该商品您现在无权访问")

        if current_user.is_authenticated:  # 已登录便加入历史
            try:
                last = History.get(History.user_id == current_user.id,
                                   History.item_id == item_id)
            except Exception as e:
                last = History(user_id=current_user.id,
                               item_id=item_id,
                               visit_time=datetime.now())
            else:
                last.visit_time = datetime.now()
            finally:
                last.save()
            # 加入：当商品状态不为0时，只有卖家和管理员可见，其他人访问返回异常提示（或404页面）（或开一个默认的，代表被下架的商品）
        return render_template('item_content.html',
                               item=item,
                               item_id=int(item_id))

    @staticmethod
    @item_blue.route('/publish/', methods=['GET'])
    @auth_func
    def publish():
        # if not current_user.is_authenticated:
        #     return render_template('404.html', message="请先登录")
        return render_template('item_publish.html')
