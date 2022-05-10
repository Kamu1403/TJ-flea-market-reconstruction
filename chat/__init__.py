#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint

chat_blue = Blueprint('chat', __name__,template_folder="templates", static_folder='/chat')
from . import models
from . import routes
from . import events
