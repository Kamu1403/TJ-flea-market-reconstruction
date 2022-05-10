<<<<<<< HEAD
###商品/悬赏管理
=======
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
>>>>>>> dccade5194ccdcf663b3b14fd61d71b5b131b9a1
from flask import Blueprint

chat_blue = Blueprint('chat', __name__,template_folder="templates", static_folder='static')
from . import models
from . import routes
from . import events
