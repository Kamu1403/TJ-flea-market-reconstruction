#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tabnanny import verbose
from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User
from item.models import Goods, Want


class Contact(BaseModel):
    """
    收件人信息类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数'''''
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="订单发起者的学号")
    name = pw.CharField(verbose_name="收件人用户名/姓名", max_length=1024)
    telephone = pw.CharField(verbose_name="收件人电话号码", max_length=32)
    addr = pw.CharField(verbose_name="收件地址", max_length=1024)


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


class Order(BaseModel):
    """
    订单类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="订单发起者的学号")
    op_user_id = pw.ForeignKeyField(User, verbose_name="对方用户的学号")
    contact_id = pw.ForeignKeyField(Contact, verbose_name="收件人信息id")
    payment = pw.DecimalField(verbose_name="总价",
                              max_digits=20,
                              decimal_places=2)
    #订单状态-1-已关闭 0-已生成 1-未确认 2-已完成
    state = pw.IntegerField(verbose_name="状态",
                            null=False,
                            default=0,
                            constraints=[pw.Check("state >=-1 AND state<=2")])

    create_time = pw.DateField(verbose_name="发布时间",
                               null=False,
                               default=datetime.utcnow())
    confirm_time = pw.DateField(verbose_name="确认时间")
    end_time = pw.DateField(verbose_name="结束时间")
    cancel_time = pw.DateField(verbose_name="取消时间")
    close_time = pw.DateField(verbose_name="关闭时间")
    note = pw.CharField(verbose_name="备注", max_length=1024)


class Order_State_Item(BaseModel):
    """
    订单状态明细类
    订单状态为已生成0时：有两个变量：买方已确认 卖方已确认。当双方都确认时，订单状态转为3。
    订单状态处于已生成0时：可以发起取消。取消立即生效。库存恢复。扣除发起方信誉分。订单状态转为已关闭（-1）。
    订单状态处于已完成2时：有两个变量：买方评价的评价id（foreign key review_id on default null）,卖方评价id。
    订单状态处于已关闭-1时：有两个变量：取消方（user_id or 管理员(80000000)），详细取消原因（取消方填，可无）
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(Order, verbose_name="订单编号")
    #订单状态为已生成0时：有两个变量：买方已确认 卖方已确认。当双方都确认时，订单状态转为3。
    user_confirm = pw.BooleanField(verbose_name="发起方是否确认",
                                   null=False,
                                   default=True)
    op_user_confirm = pw.BooleanField(verbose_name="对方是否确认",
                                      null=False,
                                      default=False)
    #订单状态处于已完成2时：有两个变量：买方评价的评价id（foreign key review_id on default null）,卖方评价id。
    user_review_id = pw.ForeignKeyField(Review, verbose_name="发起方评价ID")
    user_review_id = pw.ForeignKeyField(Review, verbose_name="发起方评价ID")
    op_user_review_id = pw.ForeignKeyField(Review, verbose_name="对方评价ID")

    #订单状态处于已关闭-1时：有两个变量：取消方（user_id or 管理员(80000000)），详细取消原因（取消方填，可无）
    cancel_user = pw.IntegerField(verbose_name="取消方的ID或管理员id")
    cancel_reason = pw.CharField(verbose_name="取消原因", max_length=1024)


class Order_Item(BaseModel):
    """
    订单明细类
    继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.IntegerField(primary_key=True)  # 主键，不显式定义的话peewee默认定义一个自增的id
    user_id = pw.ForeignKeyField(User, verbose_name="订单发起者的学号")
    op_user_id = pw.ForeignKeyField(User, verbose_name="对方用户的学号")
    order_id = pw.ForeignKeyField(Order, verbose_name="订单id")

    quantity = pw.ForeignKeyField(
        Order, verbose_name="购买数量")  #乘以单价再与订单中其他物品相加等于订单中的总价

    #与哪张表相关联取决于kind
    kind = pw.IntegerField(verbose_name="类型：悬赏还是商品", null=False,
                           default=0)  #0为商品，1为悬赏
    goods_id = pw.ForeignKeyField(Goods, verbose_name="商品id")
    want_id = pw.ForeignKeyField(Want, verbose_name="悬赏id")
