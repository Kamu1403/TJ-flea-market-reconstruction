#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_login import current_user
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request
from order.models import Order
from user.models import User_state



@order_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@order_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()

@order_blue.route('/review/<order_id>', methods=['GET', 'POST'])
def review(order_id:int):#order_id为订单ID
    print(order_id)
    try:
        get_order = Order.get(Order.id == order_id)
    except Exception as e:
        get_order = None
    if get_order is None:
        # 报错1
        flash("请求的订单不存在")
        return redirect(url_for('index'))
    else:
        print(get_order.user_id.id,get_order.op_user_id.id)
        if not current_user.is_authenticated:
            flash("请先登录")
            return redirect(url_for('user.login'))
            # 报错2
        elif current_user.id != get_order.user_id.id and current_user.id != get_order.op_user_id and current_user.state != User_state.Admin.value:
            flash("您无权访问该订单")
            return redirect(url_for('user.index'))
            # 报错3
        # return redirect(url_for('index'))
    if request.method == "POST":
        pass

    return render_template('order_review.html')
@order_blue.route('/manage', methods=['GET', 'POST'])
def manage():
    if not current_user.is_authenticated:
        flash("请先登录")
        return redirect(url_for('index'))
    else:
        try:
            print("now:{}".format(current_user.id))
            user_orders = Order.select().where(Order.user_id_id == current_user.id).execute()
            order_list = list()
            for i in user_orders:
                data = i.__data__
                data.pop('id')
                order_list.append(data)
            # 然后此数据交由前端进行显示
        except Exception as e:
            print(repr(e))
    return render_template('order_manage.html')


@order_blue.route('/generate', methods=['GET', 'POST'])
def generate():

    return render_template('order_generate.html')
