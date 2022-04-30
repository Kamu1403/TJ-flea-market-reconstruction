#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from order import order_blue
from app import database
from flask import render_template, flash, redirect, url_for, request




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
    return render_template('order_review.html')
@order_blue.route('/manage', methods=['GET', 'POST'])
def manage():
    return render_template('order_manage.html')
@order_blue.route('/generate', methods=['GET', 'POST'])
def generate():
    return render_template('order_generate.html')
