#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User
from enum import Enum,unique
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
    room_id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    receiver_id = pw.ForeignKeyField(User, verbose_name="接收者的学号")
    sender_id = pw.ForeignKeyField(User, verbose_name="发送方的学号")
    #该房间归属于发送者，是该发送者众多房间中的一个(room_id可有可无)
    



class Message(BaseModel):
    """
    聊天记录类
    记录某个房间内发生的所有聊天(发送和接收)，与房间一样，归属于发送者
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    msg_id = pw.IntegerField(primary_key=True,verbose_name="消息编号")
    msg_time = pw.DateField(verbose_name="发送时间",
                                null=False,
                                default=datetime.utcnow())
    
    room_id = pw.ForeignKeyField(Room,verbose_name="房间号")  
    sender_id = pw.ForeignKeyField(User, verbose_name="发送方的学号")

    #消息类型 0-文本类型 1-图片类型 2-系统通知类型
    msg_type = pw.IntegerField(verbose_name="消息类型", null=False, default=Msg_type.Text.value,
                                constraints=[pw.Check("msg_type >=0")])
    
    #消息内容，无论何种类型，内容都只以string形式储存
    msg = pw.CharField(verbose_name="消息内容", max_length=1024)
    
    #标记是否可见，1可见0不可见，默认1 
    visible = pw.IntegerField(verbose_name="是否显示", null=False, default=1)


class Recent_Chat_List(BaseModel):
    """
    近期消息类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    receiver_id = pw.ForeignKeyField(User,primary_key=True, verbose_name="接收者的学号")
    #将接收者视作主键
    
    last_time = pw.DateField(verbose_name="最后访问时间")
    
    unread = pw.IntegerField(verbose_name="未读条数", null=False, default=0)