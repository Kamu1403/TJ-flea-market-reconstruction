#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from flask import Flask
import peewee as pw

app = Flask(__name__,template_folder="templates")
app.config["SECRET_KEY"] = 'b8a0e5e48f7e4577a020b8502dcb7fc8'
#随机生成的秘钥，防止报错"Must provide secret_key to use csrf"

# py_peewee连接的数据库名

database = pw.MySQLDatabase(
    'tj_market',  #数据库得自己建立，peewee只有建立数据表的权限
    host='127.0.0.1',
    user='root',
    passwd='tj_market',  #记得改密码，不然你可能调试不了
    charset='utf8',
    port=3306)


class BaseModel(pw.Model):
    class Meta:
        database = database  # 将实体与数据库进行绑定


# 连接数据库
database.connect()

from item import item_blue
from user import user_blue
from admin import admin_blue
from api import api_blue
from order import order_blue
app.register_blueprint(item_blue, url_prefix='/item')
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(admin_blue,url_prefix='/admin')
app.register_blueprint(api_blue,url_prefix='/api')
app.register_blueprint(order_blue,url_prefix='/order')

from . import routes
#此处应添加创建管理员账号
