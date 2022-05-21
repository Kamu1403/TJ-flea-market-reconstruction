#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tabnanny import verbose
from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User
from item.models import Item


class Contact(BaseModel):
    """
    收件人信息类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数'''''
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="订单发起者的学号")

    #Address_json_str=pw.CharField(verbose_name="联系地址信息JSON/STR互转", max_length=1024)
    default = pw.BooleanField(
        verbose_name="是否为默认收货地址，一个user只能有一个Contact对像此字段为True",
        default=False)  #建议创建第一个的时候用True
    name = pw.CharField(verbose_name="收件人用户名/姓名", max_length=32)
    telephone = pw.CharField(verbose_name="收件人电话号码", max_length=64)
    full_address = pw.CharField(verbose_name="详细收件地址", max_length=1024)
    campus_branch = pw.CharField(
        verbose_name="所在校区",
        max_length=32,
        null=False,
        default="四平路校区",
        constraints=[
            pw.Check("campus_branch in ('四平路校区','嘉定校区','沪西校区','沪北校区')")
        ])


class Review(BaseModel):
    """
    用户评价类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="发布者的学号")
    publish_time = pw.DateField(verbose_name="发布时间",
                                null=False,
                                default=datetime.utcnow())
    feedback_content = pw.CharField(verbose_name="详细反馈", max_length=1024)


from enum import Enum, unique


#添加 unique 装饰器
@unique
class Order_state(Enum):
    #订单状态-1-已关闭 0-未确认 1-已确认(双方) 2-已完成
    Normal = 0
    Confirm = 1
    End = 2
    Close = -1


class Order(BaseModel):
    """
    订单类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="订单发起者的学号")
    op_user_id = pw.ForeignKeyField(User, verbose_name="对方用户的学号")
    contact_id = pw.ForeignKeyField(Contact, verbose_name="订单发起者信息id")
    op_contact_id = pw.ForeignKeyField(Contact, verbose_name="对方用户信息id")
    payment = pw.DecimalField(verbose_name="总价",
                              max_digits=20,
                              decimal_places=2)

    #订单状态-1-已关闭 0-未确认 1-已确认(双方) 2-已完成
    state = pw.IntegerField(verbose_name="订单状态",
                            null=False,
                            default=Order_state.Normal.value,
                            constraints=[pw.Check("state >=-1")])

    create_time = pw.DateField(verbose_name="发布时间",
                               null=False,
                               default=datetime.utcnow())
    confirm_time = pw.DateField(verbose_name="双方确认时间")  #双方都确认，才填入此项
    end_time = pw.DateField(verbose_name="完成时间")  #正常完成
    close_time = pw.DateField(verbose_name="关闭时间")  #被一方取消
    note = pw.CharField(verbose_name="备注", max_length=1024)


class Order_State_Item(BaseModel):
    """
    订单状态明细类
    订单状态为未确认 0时：有两个变量：买方已确认 卖方已确认。当双方都确认时，订单状态转为3。
    订单状态处于未确认 0时：可以发起取消。取消立即生效。库存恢复。扣除发起方信誉分。订单状态转为已关闭（-1）。
    订单状态处于已完成 2时：有两个变量：买方评价的评价id（foreign key review_id on default null）,卖方评价id。
    订单状态处于已关闭 -1时：有两个变量：取消方（user_id or 管理员(80000000)），详细取消原因（取消方填，可无）
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    order_id = pw.ForeignKeyField(Order, verbose_name="订单编号")
    #订单状态为已生成0时：有两个变量：买方已确认 卖方已确认。当双方都确认时，订单状态转为3。
    user_confirm = pw.BooleanField(verbose_name="发起方是否确认",
                                   null=False,
                                   default=True)
    op_user_confirm = pw.BooleanField(verbose_name="对方是否确认",
                                      null=False,
                                      default=False)
    #订单状态处于已完成2时：有两个变量：买方评价的评价id（foreign key review_id on default null）,卖方评价id。
    user_review_id = pw.ForeignKeyField(Review,
                                        verbose_name="发起方评价ID",
                                        null=True)
    op_user_review_id = pw.ForeignKeyField(Review,
                                           verbose_name="对方评价ID",
                                           null=True)

    #订单状态处于已关闭-1时：有两个变量：取消方（user_id or 管理员(对应管理员的ID)），详细取消原因（取消方填，可无）
    cancel_user = pw.ForeignKeyField(User,
                                     verbose_name="取消方的ID或管理员id",
                                     null=True)
    cancel_reason = pw.CharField(verbose_name="取消原因", max_length=1024)


class Order_Item(BaseModel):
    """
    订单明细类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    order_id = pw.ForeignKeyField(Order, verbose_name="订单id")
    quantity = pw.IntegerField(verbose_name="购买数量")  #乘以单价再与订单中其他物品相加等于订单中的总价
    item_id = pw.ForeignKeyField(Item, verbose_name="item id", null=True)
