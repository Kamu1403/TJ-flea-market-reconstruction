#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from distutils.log import error
from email import message
from flask_login import current_user
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request
from order.models import Order, Contact, Order_Item, Order_state
from item.models import Item, Item_state, Item_type
from user.models import User_state
import json
from functools import wraps


@order_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@order_blue.teardown_request
def teardown_request(exc):  # exc必须写上
    if not database.is_closed():
        database.close()


class OrderController:
    @staticmethod
    def auth_func(f):
        def authenticate():
            return render_template('404.html', message="请先登录", error_code=403)

        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if current_user.is_authenticated:
                return f(*args, **kwargs)
            else:
                return authenticate()

        return decorated

    @staticmethod
    @order_blue.route('/<int:order_id>/', methods=['GET'])
    def order_view(order_id: int):
        return render_template("order_view.html", order_id=order_id)

    @staticmethod
    @order_blue.route('/review/<order_id>/', methods=['GET'])
    @auth_func
    def review(order_id: int):  # order_id为订单ID
        # if not current_user.is_authenticated:
        #     return render_template('404.html', message="请先登录")
        try:
            order = Order.get(Order.id == order_id,
                              Order.state == Order_state.End.value)
        except:
            return render_template('404.html',
                                   message="未找到对应已完成订单",
                                   error_code=404)
        try:
            _order_item = Order_Item.get(Order_Item.order_id == order.id)
        except:
            return render_template('404.html',
                                   message="未找到对应已完成订单明细",
                                   error_code=404)
        if _order_item.item_id.user_id.id != current_user.id and order.user_id.id != current_user.id:  # 不是订单双方
            return render_template('404.html',
                                   message='您不是订单双方，无法评价',
                                   error_code=403)
        return render_template('order_review.html', order_id=order_id)

    @staticmethod
    @order_blue.route('/generate/<int:item_id>/', methods=['GET'])
    @auth_func
    def generate(item_id: int):
        # if not current_user.is_authenticated:
        #     return render_template('404.html', message="请先登录", error_code=403)
        try:
            item = Item.get(Item.id == item_id)
        except:
            return render_template('404.html', message="未找到该物品", error_code=404)
        if item.state == Item_state.Sale.value and item.shelved_num > 0 and item.user_id.id != current_user.id:  # 正常在售且有存量且发布者不是当前用户
            return render_template('order_generate.html', item=item)
        else:
            message = "不允许自己同自己做生意"
            if item.shelved_num <= 0:
                message = "该商品售罄"
            elif item.state != Item_state.Sale.value:
                message = "该商品或悬赏被下架或冻结"
            return render_template('404.html', message=message, error_code=403)
