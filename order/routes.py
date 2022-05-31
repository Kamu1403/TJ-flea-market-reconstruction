#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_login import current_user
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request
from order.models import Order, Contact
from item.models import Item, Item_type
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


@order_blue.route('/review/<order_id>/', methods=['GET', 'POST'])
def review(order_id: int):  #order_id为订单ID
    return render_template('order_review.html')


@order_blue.route('/manage/', methods=['GET', 'POST'])
def manage():
    return render_template('order_manage.html')


@order_blue.route('/generate/<int:item_id>/', methods=['GET', 'POST'])
def generate(item_id: int):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    try:
        item = Item.get(Item.id == item_id)
    except:
        return redirect(url_for('index'))
    if item.state == 0 and item.shelved_num > 0 and item.user_id.id != current_user.id:  #正常在售且有存量且发布者不是当前用户
        return render_template('order_generate.html')
    else:
        return redirect(url_for('index'))
