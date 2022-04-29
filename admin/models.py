#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User
  

class Feedback(BaseModel):
    """
    反馈信息
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="发布者的学号")
    publish_time = pw.DateField(verbose_name="发布时间",
                                null=False,
                                default=datetime.utcnow())

    kind=pw.IntegerField(verbose_name="反馈种类",null=False,default=0)
    #如0-举报用户或交易，1-交易出现问题 2-网站bug问题，3-个人疑问 4-个人信息有问题等
    
    #0为未读，1为已读 -1为已回复
    state = pw.IntegerField(verbose_name="状态", null=False, default=0,
                                constraints=[pw.Check("state >=-1 AND state<=1")])
    feedback_content = pw.CharField(verbose_name="详细反馈", max_length=1024)
    reply_content=pw.CharField(verbose_name="管理员回复内容", max_length=1024)

class User_Management(BaseModel):
    """
    用户管理
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="发布者的学号")
    ban_time=pw.DateField(verbose_name="解封时间",
                                null=False,
                                default=datetime.utcnow())#置当用户表中state=-1时，可以改变此项的值以实现封号时间
    ban_reason=pw.CharField(verbose_name="封号原因", max_length=1024)
