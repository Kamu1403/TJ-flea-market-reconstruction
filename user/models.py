#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from email.policy import default
from app import BaseModel
import peewee as pw
from werkzeug.security import check_password_hash
from hashlib import md5
from flask_login import UserMixin

from enum import Enum, unique

import os
import requests
from io import BytesIO
from PIL import Image

from .const import User_state,User_Campus_state,GENDER_CHECK,STATE_CHECK,CAMPUS_BRANCH_CHECK
'''
软件重构改动：将以下常量类移到config.py文件中
'''
'''
#添加 unique 装饰器
@unique
class User_state(Enum):
    #用户状态：0为普通用户，-1为封号，1为管理员
    Normal = 0
    Admin = 1
    Under_ban = -1
    
    # -1 封号
    # 0 游客
    # 1 普通用户
    # 20 管理员
    # 999 系统管理员
    


@unique
class User_Campus_state(Enum):
    SiPing = "四平路校区"
    JiaDing = "嘉定校区"
    HuXi = "沪西校区"
    HuBei = "沪北校区"
'''

class User(UserMixin, BaseModel):
    """
    用户类
    继承自UserMixin，可以方便地使用各种flask_login的API
    同时继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    用户头像统一存储在./user/static/resource/user-pic/{user-id}/avatar.WEBP
    要换头像就先把avatar.WEBP放到同目录下history文件夹中，名字随机命名，然后再把用户上传的头像压缩成jpg放在指定目录
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    username = pw.CharField(verbose_name='用户名,这里保证唯一', max_length=64, index=True, null=False, unique=True)
    email = pw.CharField(verbose_name="唯一的邮箱", max_length=128, index=True, null=False, unique=True)

    #用户状态：0为普通用户，-1为封号，1为管理员
    state = pw.IntegerField(verbose_name="状态", null=False, default=User_state.Normal.value, constraints=[pw.Check(STATE_CHECK)])
    score = pw.IntegerField(verbose_name="信誉分", default=100)  #信誉分小于零可封号

    #以下为个人信息栏
    gender = pw.CharField(verbose_name="性别", max_length=4, default='保密', constraints=[pw.Check(GENDER_CHECK)])  #三个图标

    user_no_is_published = pw.BooleanField(verbose_name="是否公开学工号", default=False)
    user_no = pw.CharField(verbose_name="学工号,字符串存储便于拓展", index=True, max_length=64)
    #应甲方要求，为方便留学生使用
    #中国用户用+86 1xx xxxx xxxx存 其他国家用其他的前缀
    telephone_is_published = pw.BooleanField(verbose_name="是否公开电话号码", default=False)
    telephone = pw.CharField(verbose_name="电话号码", max_length=64)
    wechat_is_published = pw.BooleanField(verbose_name="是否公开微信号", default=False)
    wechat = pw.CharField(verbose_name="微信号", max_length=128)
    qq_is_published = pw.BooleanField(verbose_name="是否公开QQ号", default=False)
    qq_number = pw.CharField(verbose_name="QQ号,字符串存储便于拓展", max_length=64)

    campus_is_published = pw.BooleanField(verbose_name="是否公开所在校区", default=False)
    campus_branch = pw.CharField(verbose_name="所在校区", max_length=32, null=False, default=User_Campus_state.SiPing.value, constraints=[pw.Check(CAMPUS_BRANCH_CHECK)])
    dormitory_is_published = pw.BooleanField(verbose_name="是否公开宿舍楼", default=False)
    dormitory = pw.CharField(verbose_name="所在宿舍楼", max_length=32)

    name_is_published = pw.BooleanField(verbose_name="是否公开姓名", default=False)
    name = pw.CharField(verbose_name="真实姓名", max_length=64)
    major_is_published = pw.BooleanField(verbose_name="是否公开专业", default=False)
    major = pw.CharField(verbose_name="专业", max_length=32)

    password_hash = pw.CharField(max_length=128)  #保证安全，只存密码的哈希，不存密码

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    #avatar_path 头像地址可以默认定为./resource/pic/avatar/student_number.jpg
    def create_avatar(self):  # 一个根据邮箱自动获取分形图的API，可用来作为用户头像
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        sizes = [256, 128, 64]
        url = f'https://gravatar.zeruns.tech/avatar/{digest}?d=identicon&s={sizes[0]}'
        curpath = os.path.join(os.path.dirname(__file__), 'static/resource/user-pic/')
        if not os.path.exists(os.path.join(curpath, f'{self.id}/')):
            os.makedirs(os.path.join(curpath, f'{self.id}/'))

        try:
            img = Image.open(BytesIO(requests.get(url).content))
        except:
            img = Image.open(os.path.join(curpath, f'default_avatar.jpg'))

        img.save(os.path.join(curpath, f'{self.id}/avatar.WEBP'), "WEBP")
        img.convert('RGBA')

        for size in sizes:
            img2 = img.resize((size, size))
            img2.save(os.path.join(curpath, f'{self.id}/avatar_{size}.WEBP'), "WEBP")
