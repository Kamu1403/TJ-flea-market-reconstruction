#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from admin import admin_blue
from app import database
from flask import render_template, flash, redirect, url_for, request




@admin_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@admin_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()
