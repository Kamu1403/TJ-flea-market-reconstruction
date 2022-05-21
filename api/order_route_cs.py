#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from order.models import Contact

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





@api_blue.route("/generate_order", methods=["PUT"])
def generate_order_cs():
    return make_response_json(404, "NOT FOUND")
