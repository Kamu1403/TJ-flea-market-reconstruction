#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User


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

    #   普通用户仅能看见上架数量
    #   管理员可看见上架和锁定数量
    shelved_num = pw.IntegerField(
        verbose_name="上架数量",
        null=False,
        default=1
    )
    locked_num = pw.IntegerField(
        verbose_name="锁定数量",
        null=False,
        default=0
    )

    description = pw.CharField(verbose_name="详细描述", max_length=1024)
    pic_num = pw.IntegerField(verbose_name="图片数量", null=False, default=0)
    #pic_path 商品缩略图可默认定为./resource/pic/goods/id/0.jpg 1.jpg


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

    #   普通用户仅能看见上架数量
    #   管理员可看见上架和锁定数量
    shelved_num = pw.IntegerField(
        verbose_name="上架数量",
        null=False,
        default=1
    )
    locked_num = pw.IntegerField(
        verbose_name="锁定数量",
        null=False,
        default=0
    )
    description = pw.CharField(verbose_name="详细描述", max_length=1024)
    pic_num = pw.IntegerField(verbose_name="图片数量", null=False, default=0)
    #pic_path 悬赏缩略图可默认定为./resource/pic/want/id/0.jpg 1.jpg


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
    want_id = pw.ForeignKeyField(Want, verbose_name="悬赏ID")
    collector_time = pw.DateField(verbose_name="收藏时间",
                                  default=datetime.utcnow())
