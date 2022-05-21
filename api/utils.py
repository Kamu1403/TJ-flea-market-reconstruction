#返回值规范
from typing import Dict, List
#flask
from flask_login import current_user, login_user, logout_user, login_required
from flask import make_response, request, jsonify, render_template, flash, redirect, url_for
#enum
from user.models import User_state
from admin.models import Feedback_kind, Feedback_state
from order.models import Order_state
#model
from user.models import User
from admin.models import Feedback, User_Management
from order.models import Contact, Review, Order, Order_State_Item, Order_Item
from item.models import Item, History, Favor
#common
import copy
import os
import re
import json
import datetime
import time
import random
from werkzeug.security import generate_password_hash
'''
statusCode:
•	200：操作成功返回。
•	201：表示创建成功，POST 添加数据成功后必须返回此状态码。
•	400：请求格式不对。
•	401：未授权。（User/Admin）
•	404：请求的资源未找到。
•	500：内部程序错误。

其他详见接口文档
'''

default_res = {'success': True, 'statusCode': 200, 'message': '', 'data': {}}


def make_response_json(statusCode: int = 200,
                       message: str = "",
                       data: dict = {},
                       success: bool = None,
                       quick_response: list = None):
    '''
    :params quick_response: [statusCode（若为0，则自动改为200）, message]
    如果success未指定，则当statusCode==200时为True，否则False
    '''
    if type(quick_response) == list and len(quick_response) == 2:
        statusCode = quick_response[0]
        if statusCode == 0:
            statusCode = 200
        message = quick_response[1]
    if success == None:
        success = True if statusCode // 100 == 2 else False
    return make_response(
        jsonify({
            'success': success,
            'statusCode': statusCode,
            'message': message,
            'data': data
        }))
