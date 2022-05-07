###商品/悬赏管理
from flask import Blueprint

chat_blue = Blueprint('chat', __name__,template_folder="templates", static_folder='/chat')
from . import models
from . import routes
from . import events
