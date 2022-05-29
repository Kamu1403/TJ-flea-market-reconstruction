#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from item import item_blue
from app import database
from item.models import Item, History, Favor, Item_type
from datetime import date, datetime
from flask import make_response, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user

from user.models import User_state
import json


@item_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@item_blue.teardown_request
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@item_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('item.index'))  # 重定向到/index


@item_blue.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('item_index.html')


@item_blue.route('/content/<item_id>/', methods=['GET', 'POST'])
def goods_content(item_id: int):  #goods_id/want_id
    if current_user.is_authenticated:
        try:
            last = History.get(History.user_id == current_user.id, History.item_id == item_id)
        except Exception as e:
            last = History(user_id=current_user.id, item_id=item_id, visit_time=datetime.now())
        else:
            last.visit_time = datetime.now()
        finally:
            last.save()
    return render_template('item_content.html', item_id=item_id)


@item_blue.route('/publish/', methods=['GET', 'POST'])
def publish():
    return render_template('item_publish.html')