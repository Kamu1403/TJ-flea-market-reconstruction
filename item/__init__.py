#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###商品/悬赏管理
from flask import Blueprint

item_blue = Blueprint('item', __name__,template_folder="templates", static_folder='/item')
from . import models
from . import routes
models.Goods.create_table()
models.Want.create_table()
models.HistoryGoods.create_table()
models.HistoryWant.create_table()
models.FavorGoods.create_table()
models.FavorWant.create_table()
