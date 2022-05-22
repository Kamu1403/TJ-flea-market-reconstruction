#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_login import current_user
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request
from order.models import Order,Contact
from item.models import Item, Item_type
from user.models import User_state
import json


@order_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@order_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()

@order_blue.route('/review/<order_id>/', methods=['GET', 'POST'])
def review(order_id:int):#order_id为订单ID
    try:
        get_order = Order.get(Order.id == order_id)
    except Exception as e:
        get_order = None
    if get_order is None:
        # 报错1
        flash("请求的订单不存在")
        return redirect(url_for('index'))
    else:
        if not current_user.is_authenticated:
            flash("请先登录")
            return redirect(url_for('user.login'))
            # 报错2
        elif current_user.id != get_order.user_id and current_user.id != get_order.op_user_id and current_user.state != User_state.Admin.value:
            flash("您无权访问该订单")
            return redirect(url_for('user.index'))
            # 报错3
        # return redirect(url_for('index'))
    data = get_order.__data__
    for i in data:
        if 'time' in i:
            data[i] = str(data[i])
        elif i == 'payment':
            data[i] = float(data[i])
    print(data)
    if request.method == "POST":
        pass

    return render_template('order_review.html',data = json.dumps(data))
@order_blue.route('/manage/', methods=['GET', 'POST'])
def manage():
    if not current_user.is_authenticated:
        flash("请先登录")
        return redirect(url_for('index'))
    else:
        try:
            print("now:{}".format(current_user.id))
            user_orders = Order.select().where(Order.user_id_id == current_user.id).execute()
            # 然后此数据交由前端进行显示
        except Exception as e:
            flash("获取信息出错,请联系管理员\n")
            return redirect(url_for('user.index'))
        else:
            order_list = list()
            for i in user_orders:
                data = i.__data__
                for j in data:
                    if 'time' in j:
                        data[j] = str(data[j])
                    elif i == 'payment':
                        data[j] = float(data[j])
                # data.pop('id')
                order_list.append(data)
    return render_template('order_manage.html',order_list = order_list)


@order_blue.route('/generate/<int:item_id>/', methods=['GET', 'POST'])
def generate(item_id:int):
    return render_template('order_generate.html')


