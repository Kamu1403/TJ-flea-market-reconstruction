#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from order.models import Contact
from datetime import date,timedelta

@api_blue.route("/get_order",methods=["GET"])
def get_order():
    data = dict(request.args)
    need = [Order.state==Order_state.Normal.value]
    if "range" in data:
        td = timedelta(days=int(data["range"]))
        last_time = date.today() - td
        need.append(Order.create_time>=last_time)
    try:
        need_od = Order.select().where(*need).order_by(Order.create_time.desc()).execute()
    except Exception as e:
        return make_response_json(500,f"查询发生错误 {repr(e)}")
    else:
        datas = {"wait_confirmation_op":list(),"wait_confirmation_self":list()}
        for i in need_od:
            j = i.__data__
            try:
                confirm_data = Order_State_Item.get(Order_State_Item.order_id==i['id'])
            except Exception as e:
                return make_response_json(500,f"查询发生错误 {repr(e)}")

    return make_response_json(200,"谢谢")

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


@api_blue.route("/generate_order",methods=["POST"])
def generate_order():
    data = request.get_json()
    if not current_user.is_authenticated:
        return make_response_json(401,"当前用户未登录")
    print(data)
    if "item_id" not in data:
        return make_response_json(400,"请求格式不对")
    try:
        data["item_id"] = int(data["item_id"])
        p = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(400,"请求格式不对")
    if p.shelved_num == 0:
        return make_response_json(404,"您请求的物品暂无库存")
    url = {"url":url_for('order.generate',item_id=data["item_id"])}
    return make_response_json(200,"跳转到订单生成页面",data=url)


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


@api_blue.route("/address",methods=["POST","PUT","DELETE"])
def address():
    pass

