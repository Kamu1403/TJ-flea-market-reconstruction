#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from email import message
from flask_login import current_user
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request
from order.models import Order, Contact, Order_state
from item.models import Item, Item_state, Item_type
from user.models import User_state
import json


@order_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@order_blue.teardown_request
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@order_blue.route("/<int:order_id>/", methods=["GET", "POST"])
def order_view(order_id: int):
    return render_template("order_view.html", order_id=order_id)


@order_blue.route('/review/<order_id>/', methods=['GET', 'POST'])
def review(order_id: int):  #order_id为订单ID
    if not current_user.is_authenticated:
        return render_template('404.html', message="请先登录")
    try:
        order = Order.get(Order.id == order_id,
                          Order.state == Order_state.End.value)
    except:
        return render_template('404.html', message="未找到对应已完成订单")

    return render_template('order_review.html')


@order_blue.route('/generate/<int:item_id>/', methods=['GET', 'POST'])
def generate(item_id: int):
    if not current_user.is_authenticated:
        return render_template('404.html', message="请先登录")
    try:
        item = Item.get(Item.id == item_id)
    except:
        return render_template('404.html', message="未找到该物品")
    if item.state == Item_state.Sale.value and item.shelved_num > 0 and item.user_id.id != current_user.id:  #正常在售且有存量且发布者不是当前用户
        return render_template('order_generate.html', item=item)
    else:
        message = "不允许自己同自己做生意"
        if item.shelved_num <= 0:
            message = "该商品售罄"
        elif item.state != Item_state.Sale.value:
            message = "该商品或悬赏被下架或冻结"
        return render_template('404.html', message=message)
