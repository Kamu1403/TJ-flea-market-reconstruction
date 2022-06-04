#返回值规范
from typing import Dict, List
#flask
from flask_socketio import emit, join_room, leave_room
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
from item.models import Item, History, Favor, Item_type, Item_state
from chat.models import Room,Message,Recent_Chat_List


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
    
    
def send_message(sender,receiver,message):
    time= datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    emit('alert', {'msg': sender + ':' + message,
                    'time':time,
                    'type':'text'},
        room=receiver,
        namespace='/chat')
    
    roomid = message['room']
    
    state=Room.get_or_none(Room.room_id==roomid)
    
    read=0
    if (state==None):
        pass
    elif state.room_state==2:
        read=1
    
    if read==0:
        if Recent_Chat_List.get_or_none(receiver_id=message['receiver'])==None:
            Recent_Chat_List.insert(
            receiver_id=message['receiver'],
            sender_id=sender,
            last_time=message['time'],
            last_msg=message['msg'],
            unread=1).execute()
        else:
            Recent_Chat_List.update(
            last_time=message['time'],
            last_msg=message['msg'],
            unread=Recent_Chat_List.unread+1).where(Recent_Chat_List.receiver_id==message['receiver'] and Recent_Chat_List.sender_id==sender).execute()
            
            Recent_Chat_List.update(
            last_time=message['time'],
            last_msg=message['msg'],).where(Recent_Chat_List.receiver_id==sender and Recent_Chat_List.sender_id==message['receiver']).execute()
        
    Message.create(
                msg_time=message['time'],
                room_id=roomid,
                sender_id=sender,
                msg_type=message['type'],
                msg_content=message['msg'],
                msg_read=read)
    
    Room.update(last_message=message['msg'],last_sender_id=sender).where(Room.room_id==roomid).execute()
    
    emit('message', {'msg': sender + ':' + message['msg'],
                     'other_user':message['receiver'],
                     'time':message['time'],
                     'type':message['type']},
         room=sender)
    
    emit('message', {'msg': sender + ':' + message['msg'],
                     'other_user':sender,
                     'time':message['time'],
                     'type':message['type']},
         room=message['receiver'])
    
        
    #在message外需要新增事件notice，作用：在一方输入后更新另一方的聊天列表显示
    print(sender)
    if not database.is_closed():
        database.close()
