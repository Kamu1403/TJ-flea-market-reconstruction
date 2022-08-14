#返回值规范
from asyncio.windows_events import NULL
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
from item.models import Item, History, Favor, Item_type, Item_state, Item_tag_type
from chat.models import Room, Message, Recent_Chat_List

from chat.routes import create_or_update_meet_list
#common
import copy
import os
import re
import json
import datetime
import time
import random
from werkzeug.security import generate_password_hash
from numpy import float32 as Float
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
SYS_ADMIN_NO = 80000000

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
    return make_response(jsonify({'success': success, 'statusCode': statusCode, 'message': message, 'data': data}))


def send_message(sender: str | int, receiver: str | int, message: str, type: int = 0):
    '''
    直接从后端发送消息
    :params type:0为文本,1为图片
    '''
    try:
        sender = str(sender)
        receiver = str(receiver)

        create_or_update_meet_list(sender, receiver)
        create_or_update_meet_list(receiver, sender)

        time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        room = sender + '-' + receiver
        reroom = receiver + '-' + sender
        if (sender != receiver):
            roomid = Room.get_or_none(Room.room_id == room)
            reroomid = Room.get_or_none(Room.room_id == reroom)
            if (roomid == None and reroomid == None):
                Room.create(room_id=room, last_sender_id=sender)
            elif reroomid != None:
                room = reroom

        state = Room.get_or_none(Room.room_id == room)

        read = 0
        if (state == None):
            pass
        elif state.room_state == 2:
            read = 1

        if read == 0:
            if Recent_Chat_List.get_or_none(receiver_id=receiver) == None:
                Recent_Chat_List.insert(receiver_id=receiver,
                                        sender_id=sender,
                                        last_time=time,
                                        last_msg=message,
                                        unread=1).execute()
            else:
                Recent_Chat_List.update(
                    last_time=time,
                    last_msg=message,
                    unread=Recent_Chat_List.unread + 1).where(
                        Recent_Chat_List.receiver_id == receiver
                        and Recent_Chat_List.sender_id == sender).execute()

                Recent_Chat_List.update(
                    last_time=time,
                    last_msg=message,
                ).where(Recent_Chat_List.receiver_id == sender
                        and Recent_Chat_List.sender_id == receiver).execute()

        Message.create(msg_time=time,
                       room_id=room,
                       sender_id=sender,
                       msg_type=type,
                       msg_content=message,
                       msg_read=read)

        Room.update(
            last_message=message,
            last_sender_id=sender,
            msg_type=type).where(Room.room_id == room).execute()


        emit('message', {
            'sender': sender,
            'msg': message,
            'other_user': receiver,
            'time': time,
            'type': type
        },
            room=sender,
            namespace='/chat')
        
        if (read==1):
            emit('message', {
                'sender': sender,
                'msg': message,
                'other_user': sender,
                'time': time,
                'type': type
            },
                room=receiver,
                namespace='/chat')
        else:
            emit('notice', {
                'sender': sender,
                'msg': message,
                'other_user': sender,
                'time': time,
                'type': type
            },
                room=receiver,
                namespace='/chat')
        return (200, "操作成功")
    except Exception as e:
        return (500, repr(e))



def getItem(data,name):
    try:
        data["item_id"] = int(data["item_id"])
        data[name] = int(data[name])
    except Exception as e:
        return (-1,400, "请求格式不对",NULL)
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return (-1,404, "此商品不存在",NULL)
    #全都成功
    return (0,0,"" ,item)

def checkWrongItemOperation(current_user,data,item):
    if current_user.state == User_state.Under_ban.value:
        return (-1,401, "您当前已被封号,请联系管理员解封")
    else:
        if current_user.id != item.user_id_id:
            return (-1,401, "不可改变其他人的商品状态")
        else:
            if data["state"] == Item_state.Freeze.value:
                return (-1,401, "权限不足")
            else:
                return (0,0,"操作成功")

def checkItemData(data):
    if len(data["name"])>40:
        return (-1,400,"名称过长")
    if len(data["description"]) > Item.description.max_length:
        return (-1,400,f"描述过长,应限制在{Item.description.max_length}字以内")
    if "tag" not in data:
        return (-1,400, "请选择物品类型")
    if data["tag"] not in Item_tag_type._value2member_map_:
        return (-1,400, "请求格式错误")
    try:
        price = Float(data["price"])
        if "type" in data:
            item_type = int(data["type"])
        shelved_num = int(data["shelved_num"])
    except Exception as e:
        #return (-1,400, "数据类型错误")
        return (-1,400, str(e))
    if price == Float("inf") or price == Float("nan"):
        return (-1,400, "价格越界")
    if price <= 1e-8:
        return (-1,400, "价格越界")
    if "type" in data:
        if item_type != Item_type.Goods.value and item_type != Item_type.Want.value:
            return (-1,400, "仅能上传物品")
    if shelved_num <= 0:
        return (-1,400, "数量越界")
    if shelved_num.bit_length() > Item.shelved_num.__sizeof__()-1:
        return (-1,400, "数量越界")
    return (0,0,"")