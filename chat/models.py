#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
import json
from datetime import datetime
from user.models import User
from enum import Enum,unique

class JSONField(pw.TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


#添加 unique 装饰器
@unique
class Msg_type(Enum):
    #消息类型 0-文本类型 1-图片类型 2-系统通知类型
    Text = 0
    Image = 1
    Notice=2

class Room(BaseModel):
    """
    聊天室类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    room_id = pw.CharField(primary_key=True)  
    # 主键，该房间归属于通信双方，主键使用 user1_id '+' user2_id 记录
    room_state =pw.IntegerField(verbose_name="房间状态",default=0,null=False,
                                constraints=[pw.Check("room_state >=0")])
    #房间状态 0-无人使用 1-单人使用 2-双方使用
    last_message =pw.CharField(verbose_name="最后消息")
    # 该房间内产生的最后一次通信记录，可以为空



class Message(BaseModel):
    """
    聊天记录类
    记录某个房间内发生的所有聊天(发送和接收)，与房间一样，归属于发送者
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    msg_id = pw.AutoField(primary_key=True,verbose_name="消息编号")
    msg_time = pw.DateTimeField(verbose_name="发送时间",
                                null=False,
                                default=datetime.utcnow())
    
    room_id = pw.ForeignKeyField(Room,verbose_name="房间号")  
    
    sender_id = pw.ForeignKeyField(User, verbose_name="发送方的id")

    #消息类型 0-文本类型 1-图片类型 2-系统通知类型
    msg_type = pw.IntegerField(verbose_name="消息类型", null=False, default=Msg_type.Text.value,
                                constraints=[pw.Check("msg_type >=0")])
    
    #消息内容，无论何种类型，内容都只以string形式储存
    msg_content = pw.CharField(verbose_name="消息内容", max_length=1024)
    
    #标记是否已读，1已读0未读，默认0
    msg_read = pw.IntegerField(verbose_name="是否已读", null=False, default=0)
    
    #标记是否可见，1可见0不可见，默认1
    sender_visible = pw.IntegerField(verbose_name="发送方是否显示", null=False, default=1)
    receiver_visible = pw.IntegerField(verbose_name="接收方是否显示", null=False, default=1)


class Recent_Chat_List(BaseModel):
    """
    近期消息类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    receiver_id = pw.ForeignKeyField(User, verbose_name="接收者的id")
    sender_id = pw.ForeignKeyField(User, verbose_name="发送者的id")
    
    last_msg = pw.CharField(verbose_name="最后消息")
    last_time = pw.DateTimeField(verbose_name="最后访问时间")
    
    unread = pw.IntegerField(verbose_name="未读条数", null=False, default=0)

class Meet_List(BaseModel):
    """
    会话列表类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    user_id=pw.ForeignKeyField(User, primary_key=True,verbose_name="登录用户的id")
    meet_list=JSONField(verbose_name="会话列表")