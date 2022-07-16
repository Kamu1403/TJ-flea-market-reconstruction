#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User

from enum import Enum, unique


#添加 unique 装饰器
@unique
class Item_state(Enum):
    #物品状态 -1-被管理员冻结，无法搜素 0-正常在售(无论上架数量是否为0) 1-商品被上架人自己下架，无法被搜索
    Sale = 0
    Freeze = -1
    Lock = 1


@unique
class Item_type(Enum):
    #物品类型 0-商品 1-悬赏
    Goods = 0
    Want = 1

@unique
class Item_tag_type(Enum):
    tag_1 = '家用电器'
    tag_2 = '手机/运营商/数码'
    tag_3 = '电脑/办公'
    tag_4 = '家居/家具/家装/厨具'
    tag_5 = '男装/女装/童装/内衣'
    tag_6 = '美妆/个护清洁/宠物'
    tag_7 = '女鞋/箱包/钟表/珠宝'
    tag_8 = '男鞋/运动/户外'
    tag_9 = '房产/汽车/汽车用品'
    tag_10 = '母婴/玩具乐器'
    tag_11 = '食品/酒类/生鲜/特产'
    tag_12 = '艺术/礼品鲜花/农资绿植'
    tag_13 = '医药保健/计生情趣'
    tag_14 = '图书/文娱/教育/电子书'
    tag_15 = '机票/酒店/旅游/生活'
    tag_16 = '理财/众筹/白条/保险'
    tag_17 = '安装/维修/清洗/二手'
    tag_18 = '工业品'
    tag_19 = "其他"

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
    publish_time = pw.DateTimeField(verbose_name="发布时间",
                                null=False,
                                default=datetime.now())
    price = pw.FloatField(verbose_name="单价", default=0, null=False)
    tag = pw.CharField(verbose_name="Tag,用于分类", max_length=128, index=True)
    state = pw.IntegerField(verbose_name="物品状态",
                            default=Item_state.Sale.value,
                            constraints=[pw.Check("state >=-1")])
    type = pw.IntegerField(verbose_name="物品类型：悬赏或商品",
                           default=Item_type.Goods.value,
                           constraints=[pw.Check("type>=-1")])

    #   普通用户仅能看见上架数量
    #   管理员可看见上架和锁定数量
    shelved_num = pw.IntegerField(verbose_name="上架数量", null=False, default=1)
    locked_num = pw.IntegerField(verbose_name="锁定数量", null=False, default=0)

    description = pw.CharField(verbose_name="详细描述", max_length=1024)

    #pic_num = pw.IntegerField(verbose_name="图片数量", null=False, default=0)
    #商品缩略图默认存储在 ./item/static/resource/item-pic/{item-id}/缩略图/{pic_num个文件}


class History(BaseModel):
    """
    历史记录类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="访问者的id")
    item_id = pw.ForeignKeyField(Item, verbose_name="item ID")
    visit_time = pw.DateTimeField(verbose_name="访问时间", default=datetime.now())


class Favor(BaseModel):
    """
    收藏类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="收藏者的id")
    item_id = pw.ForeignKeyField(Item, verbose_name="item ID")
    collect_time = pw.DateTimeField(verbose_name="收藏时间", default=datetime.now())
