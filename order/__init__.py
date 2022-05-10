#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###订单

from flask import Blueprint

order_blue = Blueprint('order', __name__,template_folder="templates",static_folder="static")
from . import models
from . import routes
