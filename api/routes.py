#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api import api_blue
from app import database
from flask import render_template, flash, redirect, url_for, request




@api_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@api_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()


@api_blue.route("/delete")
def delete_api():
    return 'delete'
@api_blue.route('/put')
def put_api():
    return 'put!'
@api_blue.route('/post')
def post_api():
    return 'put!'
@api_blue.route('/get')
def get_api():
    return 'put!'
