#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

###管理员
from flask import Blueprint

admin_blue = Blueprint('admin', __name__,static_folder="static",template_folder="templates")
from . import models
from . import routes
