#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User

from enum import Enum,unique
#添加 unique 装饰器
@unique
class Item_state(Enum):
    #物品状态 -1-被管理员冻结，无法搜素 0-正常在售(无论上架数量是否为0) 1-商品被上架人自己下架，无法被搜索
    Sale = 0
    Freeze = -1
    Lock=1
@unique
class Item_type(Enum):
    #物品类型 0-商品 1-悬赏
    Goods = 0
    Want =1


class Item(BaseModel):
    """
    商品/悬赏类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    name = pw.CharField(verbose_name="商品名",
                        max_length=128,
                        index=True,
                        null=False)
    user_id = pw.ForeignKeyField(User, verbose_name="发布者的id")
    publish_time = pw.DateField(verbose_name="发布时间",
                                null=False,
                                default=datetime.utcnow())
    price = pw.FloatField(verbose_name="单价", default=0,null=False)
    tag=pw.CharField(verbose_name="Tag,用于分类",max_length=128,index=True)
    state=pw.IntegerField(verbose_name="物品状态",default=Item_state.Sale.value,constraints=[pw.Check("state >=-1")])
    type=pw.IntegerField(verbose_name="物品类型：悬赏或商品",default=Item_type.Goods.value,constraints=[pw.Check("type>=-1")])

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
    #商品缩略图默认存储在 ./item/static/resource/item-pic/{item-id}/{pic_num个文件}

class History(BaseModel):
    """
    历史记录类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="访问者的id")
    item_id = pw.ForeignKeyField(Item, verbose_name="item ID")
    visit_time = pw.DateField(verbose_name="访问时间", default=datetime.utcnow())

class Favor(BaseModel):
    """
    收藏类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="收藏者的id")
    item_id = pw.ForeignKeyField(Item, verbose_name="item ID")
    collect_time = pw.DateField(verbose_name="收藏时间", default=datetime.utcnow())
