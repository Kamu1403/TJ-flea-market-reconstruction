#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###管理员
from flask import Blueprint

admin_blue = Blueprint('admin', __name__,static_folder="admin")
from . import models
from . import routes
models.Feedback.create_table()
models.User_Management.create_table()
