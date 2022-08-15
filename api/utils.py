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
from PIL import Image
from hashlib import md5

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

# 对用户的检查
def check_user(user, admin_power_check = False, ban_check = False):
    if not user.is_authenticated:
        return -1, make_response_json(401, "该用户未通过验证或未登录")
    if admin_power_check and user.state != User_state.Admin.value:
        return -1, make_response_json(401, "权限不足")
    if ban_check and user.state == User_state.Under_ban.value:
        return -1, make_response_json(401, "当前用户已被封禁")

    return 0, 0


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
        return (-1,400, "数据类型错误")
        #return (-1,400, str(e))
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


def createPath(path: str) -> None:
    # 当前路径不存在，直接建立文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    # 路径存在但不是文件夹，将其删除后创建新的文件夹
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)

def savePic(data,curpath):
    path_name = os.path.join(curpath, data.filename)
    createPath(curpath)
    data.save(path_name)
    img = Image.open(path_name)
    w, h = img.size
    # 长宽中较大的/1920作为比率
    ratio = max(w, h) / 1920
    #比率达于1，按照比率缩放,使得最大的到达1920
    if ratio > 1:
        img = img.resize((int(w / ratio), int(h / ratio)))
    ratio = 250 / min(w, h)
    #按比例缩放使得图片长宽较小者大于等于250
    if ratio > 1:
        img = img.resize((int(w * ratio), int(h * ratio)))
    md5_str = md5(img.tobytes()).hexdigest()
    os.remove(path_name)
    #创建新的图片路径并保存
    path_name_new = os.path.join(curpath, f'{md5_str}')
    img.save(path_name_new, 'WEBP')
    img = Image.open(path_name_new)
    md5_str = md5(img.tobytes()).hexdigest()
    os.remove(path_name_new)

    path_name_new = os.path.join(curpath, f'{md5_str}')
    #if os.path.exists(path_name_new):
    #    return make_response_json(400, f"上传图片失败：请勿重复上传图片")
    img.save(path_name_new, 'WEBP')
    return md5_str


#获取favor和history列表的一些函数
def getRange(req):
    if "range_min" in req or "range_max" in req:
        if "range_min" in req and "range_max" in req:
            try:
                range_min = int(req["range_min"])
                range_max = int(req["rang_max"])
            except Exception as e:
                return (-1,400, "请求格式错误")
        else:
            return (-1,400,"请求格式错误")
    else:
        range_min = 0
        range_max = 50
    return (0,range_min,range_max)

def getFSList(myclass,listname):
    if listname=="favor_list":
        tep = myclass.select().where(myclass.user_id == current_user.id).order_by(
            myclass.collect_time.desc())
    else:
        tep = myclass.select().where(myclass.user_id == current_user.id).order_by(
            myclass.visit_time.desc())
    fav_data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        if listname=="favor_list":
            res['collect_time'] = str(i.collect_time)
        else:
            res['visit_time'] = str(i.visit_time)
        fav_data.append(res)
    return fav_data

def getFS(myclass,req,listname):
    #取范围
    result=getRange(req)
    if result[0]==-1:
        return (-1,result[1], result[2])
    range_min=result[1]
    range_max=result[2]
    #添加data
    fav_data=getFSList(myclass,listname)
    data = {
        "total_count": len(fav_data),
        listname: fav_data[range_min:range_max]
    }
    return (0,data)

def delFS(myclass,req):
    try:
        NotFound = False
        for i in req:
            tep = myclass.select().where((myclass.user_id == current_user.id)
                                         & (myclass.item_id == i))

            if tep.count() <= 0:
                NotFound = True
            else:
                myclass.delete().where((myclass.user_id == current_user.id)
                                       & (myclass.item_id == i)).execute()
        if NotFound == True:
            if myclass==History:
                return (404, "不存在对应的历史")
            else:
                return (404, "不存在对应的收藏")
        return (200, "删除成功")
    except Exception as e:
        return(500, f"发生错误 {repr(e)}")