#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from statistics import quantiles
from tkinter import E
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from order.models import Contact

@api_blue.route("/get_order",methods=["GET"])
def get_order():
    pass

@api_blue.route("/get_address",methods=['GET'])
def get_address():
    if not current_user.is_authenticated:
        return make_response_json(401,"当前用户未登录")
    elif current_user.state == User_state.Under_ban.value:
        return make_response_json(401,"当前用户已被封禁")
    need = [Contact.name,Contact.telephone,Contact.full_address,Contact.default,Contact.campus_branch]
    try:
        datas = Contact.select(*need).where(Contact.user_id==current_user.id).execute()
    except Exception as e:
        return make_response_json(500,f"发生如下错误\n{repr(e)}")
    else:
        data = list()
        for i in datas:
            data.append(i.__data__)
        if len(data) == 0:
            return make_response_json(404,"该用户未设置任何联系地址")
    return make_response_json(200,"获取成功",data)


#@api_blue.route("/")


@api_blue.route("/order_post", methods=["POST"])
def order_post():
    data = request.get_json()
    try:
        data["num"] = int(data["num"])
    except Exception as e:
        return make_response_json(400,"请指定物品个数")
    if not current_user.is_authenticated:
        return make_response_json(401,"当前用户未登录")
    if current_user.state == User_state.Under_ban.value:
        return make_response_json(401,"当前用户被封禁中")
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(400,"不存在此款物品")
    if item.shelved_num < data["num"]:
        return make_response_json(401,"物品库存不足")
    if current_user.id == item.user_id.id:
        return make_response_json(401,"不可自己和自己做生意")
    try:
        contact = Contact.get(Contact.id == data["contact_id"])
    except Exception as e:
        return make_response_json(400,"您指定的联系方式不存在")
    try:
        op_contact = Contact.get(Contact.user_id == item.user_id.id,Contact.default==True)
    except Exception as e:
        return make_response_json(400,"对方未存储联系方式")
    try:
        order_data = dict()
        order_data["user_id"] = current_user.id
        order_data["op_user_id"] = item.user_id.id
        order_data["contact_id"] = data["contact_id"]
        order_data["op_contact_id"] = op_contact.id
        order_data["note"] = data["note"]
        order_data["payment"] = item.price*data["num"]
        od = Order.create(**order_data)
    except Exception as e:
        return make_response_json(500,f"存储错误\n{repr(e)}")
    else:
        try:
            od_it = Order_Item.create(order_id=od.id,quantity=data["num"],item_id=item.id)
        except Exception as e:
            od.delete_instance()
            return make_response_json(500,f"存储错误\n{repr(e)}")
        else:
            try:
                Order_State_Item.create(order_id=od.id)
            except Exception as e:
                od_it.delete_instance()
                od.delete_instance()
                return make_response_json(500,f"存储错误\n{repr(e)}")
    return make_response_json(200, "订单生成成功，请等待商家确认",data=url_for("order.manage"))
