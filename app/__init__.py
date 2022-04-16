#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_login import LoginManager
from flask import Flask
import peewee as pw

app = Flask(__name__)
app.config["SECRET_KEY"] = 'b8a0e5e48f7e4577a020b8502dcb7fc8'
#随机生成的秘钥，防止报错 Must provide secret_key to use csrf

login = LoginManager(app)

# py_peewee连接的数据库名

db = pw.MySQLDatabase(
    'tj_market',  #数据库得自己建立，peewee只有建立数据表的权限
    #host='localhost',
    host='127.0.0.1',
    user='root',
    passwd='tongjigzy_02',
    charset='utf8',
    port=3306)


class BaseModel(pw.Model):
    class Meta:
        database = db  # 将实体与数据库进行绑定


from app import models  ##这一行必须在这里，不能移到上面去
# 连接数据库
db.connect()

# 创建数据表

models.User.create_table()
models.Goods.create_table()
models.Want.create_table()
models.HistoryGoods.create_table()
models.HistoryWant.create_table()
models.FavorGoods.create_table()
models.FavorWant.create_table()
