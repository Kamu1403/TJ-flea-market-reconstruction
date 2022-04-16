#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tabnanny import verbose
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin
from app import BaseModel
import peewee as pw

from datetime import datetime


class User(UserMixin, BaseModel):
    """
    用户类
    继承自UserMixin，可以方便地使用各种flask_login的API
    同时继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    student_number = pw.IntegerField(verbose_name="学号,作为主键使用",
                                     primary_key=True)
    username = pw.CharField(verbose_name='用户名,这里保证唯一',
                            max_length=64,
                            index=True,
                            null=False,
                            unique=True)
    email = pw.CharField(verbose_name="唯一的邮箱",
                         max_length=128,
                         index=True,
                         null=False,
                         unique=True)
    score = pw.IntegerField(verbose_name="信誉分", default=100)

    #应甲方要求，为方便留学生使用
    #中国用户用+86 1xx xxxx xxxx存 其他国家用其他的前缀
    telephone = pw.CharField(verbose_name="电话号码", max_length=32, unique=True)
    wechat = pw.CharField(verbose_name="微信号", max_length=128, unique=True)
    qq_number = pw.IntegerField(verbose_name="QQ号", unique=True)

    campus_branch = pw.CharField(
        verbose_name="所在校区",
        max_length=32,
        default="四平路校区",
        constraints=[
            pw.Check("campus_branch in ('四平路校区','嘉定校区','沪西校区','沪北校区')")
        ])
    dormitory = pw.CharField(verbose_name="所在宿舍楼", max_length=32)
    #理论宿舍楼宇名字这里也应该写个check，保证他们不乱填，但是不熟，摸了

    gender_is_published = pw.BooleanField(verbose_name="是否公开性别", default=True)
    gender = pw.CharField(verbose_name="性别",
                          max_length=4,
                          constraints=[pw.Check("gender in ('男', '女')")])
    name_is_published = pw.BooleanField(verbose_name="是否公开姓名", default=True)
    name = pw.CharField(verbose_name="真实姓名", max_length=16)
    major_is_published = pw.BooleanField(verbose_name="是否公开专业", default=True)
    major = pw.CharField(verbose_name="专业", max_length=32)
    password_hash = pw.CharField(max_length=128)  #保证安全，只存密码的哈希，不存密码

    def set_password(self, password):
        self.password_hash = str(generate_password_hash(password))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    #avatar_path 头像地址可以默认定为./resource/pic/avatar/student_number.jpg
    def avatar(self, size):  # 一个根据邮箱自动获取分形图的API，可用来作为用户头像
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.zeruns.tech/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Goods(BaseModel):
    """
    商品类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    name = pw.CharField(verbose_name="商品名",
                        max_length=128,
                        index=True,
                        null=False)
    publisher_id = pw.ForeignKeyField(User, verbose_name="发布者的学号")
    publish_time = pw.DateField(verbose_name="发布时间",
                                null=False,
                                default=datetime.utcnow())
    price = pw.FloatField(verbose_name="价格", index=True, null=False)
    status = pw.IntegerField(
        verbose_name="商品状态",
        index=True,
        null=False,
        constraints=[pw.Check("status>=0 AND status<=2")],
        default=0)  #0为上架(未交易)，1为锁定(正在交易)，2为下架(交易完成或被商家、管理员下架)
    description = pw.CharField(verbose_name="详细描述", max_length=1024)
    pic_num = pw.IntegerField(verbose_name="图片数量", null=False, default=0)
    #pic_path 商品缩略图可默认定为./resource/pic/goods/id-0.jpg id-1.jpg


class Want(BaseModel):
    """
    悬赏类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    name = pw.CharField(verbose_name="悬赏名",
                        max_length=128,
                        index=True,
                        null=False)
    publisher_id = pw.ForeignKeyField(User, verbose_name="发布者的学号")
    publish_time = pw.DateField(verbose_name="发布时间", default=datetime.utcnow())
    price = pw.FloatField(verbose_name="价格", index=True, null=False)
    status = pw.IntegerField(
        verbose_name="悬赏状态",
        index=True,
        null=False,
        constraints=[pw.Check("status>=0 AND status<=2")],
        default=0)  #0为上架(未交易)，1为锁定(正在交易)，2为下架(交易完成或被商家、管理员下架)
    description = pw.CharField(verbose_name="详细描述", max_length=1024)
    pic_num = pw.IntegerField(verbose_name="图片数量", null=False, default=0)
    #pic_path 悬赏缩略图可默认定为./resource/pic/want/id-0.jpg id-1.jpg


class HistoryGoods(BaseModel):
    """
    历史记录类（商品）
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    visitor_id = pw.ForeignKeyField(User, verbose_name="访问者的学号")
    goods_id = pw.ForeignKeyField(Goods, verbose_name="商品ID")
    visitor_time = pw.DateField(verbose_name="访问时间", default=datetime.utcnow())


class HistoryWant(BaseModel):
    """
    历史记录类（悬赏）
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    visitor_id = pw.ForeignKeyField(User, verbose_name="访问者的学号")
    want_id = pw.ForeignKeyField(Want, verbose_name="悬赏ID")
    visitor_time = pw.DateField(verbose_name="访问时间", default=datetime.utcnow())


class FavorGoods(BaseModel):
    """
    收藏类(商品)
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    collector_id = pw.ForeignKeyField(User, verbose_name="收藏者的学号")
    goods_id = pw.ForeignKeyField(Goods, verbose_name="商品ID")
    collector_time = pw.DateField(verbose_name="收藏时间",
                                  default=datetime.utcnow())


class FavorWant(BaseModel):
    """
    收藏类(悬赏)
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    collector_id = pw.ForeignKeyField(User, verbose_name="收藏者的学号")
    want_id = pw.ForeignKeyField(Want, verbose_name="商品ID")
    collector_time = pw.DateField(verbose_name="收藏时间",
                                  default=datetime.utcnow())
