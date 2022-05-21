#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###api管理
from flask import Blueprint

api_blue = Blueprint('api', __name__,template_folder="templates", static_folder='static')

from . import routes
from . import item_routes
from . import chat_routes