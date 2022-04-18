#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###用户、收藏、历史

from flask import Blueprint

user_blue = Blueprint('order', __name__,static_folder="order")
from . import models
from . import routes
#models.Order.create_table()
