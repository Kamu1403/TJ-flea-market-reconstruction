#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#导入设置
import config

database_name = config.database_name
password = config.password
user = config.user
ipaddr=config.ipaddr

#用pymysql创建数据库
from . import create_database
if config.drop_database == True:
    create_database.create_database(database_name, password, user,ipaddr)

#创建app
from flask import Flask

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = 'b8a0e5e48f7e4577a020b8502dcb7fc8'
#随机生成的秘钥，防止报错"Must provide secret_key to use csrf"
app.config['JSON_AS_ASCII'] = False

from flask_socketio import SocketIO

socketio = SocketIO()
socketio.init_app(app)

import peewee as pw
# py_peewee连接的数据库名:database
database = pw.MySQLDatabase(
    database=database_name,
    host=ipaddr,
    user=user,
    passwd=password,  #记得改密码，不然你可能调试不了
    charset='utf8',
    port=3306)


class BaseModel(pw.Model):

    class Meta:
        database = database  # 将实体与数据库进行绑定


# 连接数据库
database.connect()

#所有蓝图
from item import item_blue
from user import user_blue
from admin import admin_blue
from api import api_blue
from order import order_blue
from chat import chat_blue

app.register_blueprint(item_blue, url_prefix='/item')
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(admin_blue, url_prefix='/admin')
app.register_blueprint(api_blue, url_prefix='/api')
app.register_blueprint(order_blue, url_prefix='/order')
app.register_blueprint(chat_blue, url_prefix='/chat')

#初始化数据库
from . import init_database

init_database.init_database(config.drop_database)

#app目录的路由
from . import routes
