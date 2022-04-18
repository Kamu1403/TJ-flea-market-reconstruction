#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###用户、收藏、历史

from flask import Blueprint

user_blue = Blueprint('user', __name__,static_folder="user")
from . import models
from . import routes
models.User.create_table()
