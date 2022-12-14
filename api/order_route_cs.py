#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from user.models import User_Campus_state
from item.models import Item_type, Item_state
from order.models import Contact
from datetime import datetime, timedelta




@api_blue.route("/get_order", methods=["GET"])
def get_order():
    #用户未登录处理
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = dict(request.args)
    my_order = [
        (Order.user_id == current_user) | (Item.user_id == current_user.id)
    ]
    if "range" in data:
        try:
            data["range"] = int(data["range"])
        except Exception as e:
            return make_response_json(400, "请求格式错误")
        else:
            td = timedelta(days=data["range"])
            last_time = datetime.now() - td
            my_order.append(Order_Item.order_id.create_time >= last_time)
    try:
        my_od_item = Order_Item.select(Order_Item.order_id,Order_Item.item_id)\
        .join(Order,on=(Order.id==Order_Item.order_id)).join(Item,on=(Item.id==Order_Item.item_id))\
        .where(*my_order).order_by(
            Order_Item.order_id.create_time.desc())
    except Exception as e:
        return make_response_json(500, f"查询发生错误 {repr(e)}")
    else:
        datas = list()
        order_set = dict()
        for j in my_od_item:
            if j.order_id.id not in order_set:
                order_set[j.order_id.id] = len(datas)
                datas.append({"order_id":j.order_id.id,"user_id":j.order_id.user_id.id\
                    ,"op_user_id":j.item_id.user_id.id,"item_id_list":list(),"state":j.order_id.state})
            if j.item_id.id not in datas[order_set[
                    j.order_id.id]]["item_id_list"]:
                datas[order_set[j.order_id.id]]["item_id_list"].append(
                    j.item_id.id)
    return make_response_json(200, "返回订单", datas)


@api_blue.route("/get_order_info", methods=['GET'])
def get_order_info():
    #用户未登录处理
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = dict(request.args)
    try:
        order_id = int(data["order_id"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        temp: Order_Item = Order_Item.get(Order_Item.order_id == order_id)
    except Exception as e:
        return make_response_json(404, "不存在该订单")
    if current_user.id != temp.item_id.user_id.id and current_user.id != temp.order_id.user_id.id and current_user.state != User_state.Admin.value:
        return make_response_json(401, "当前用户无权访问该订单信息")
    order_data = temp.order_id.__data__
    order_data.pop("id")
    for i in order_data:
        if "time" in i:
            order_data[i] = str(order_data[i])
    order_data["item_info"] = list()
    try:
        item_infos = Order_Item.select().where(
            Order_Item.order_id == order_id).execute()
    except Exception as e:
        return make_response_json(500, f"查询订单明细时出现问题 {repr(e)}")
    for i in item_infos:
        j = i.__data__
        j.pop("id")
        j.pop("order_id")
        order_data["item_info"].append(j)
    return make_response_json(200, "请求成功", order_data)


@api_blue.route("/get_address", methods=['GET'])
def get_address():
    res = check_user(current_user, False, True)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    elif current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户已被封禁")
    '''
    need = [
        Contact.id, Contact.name, Contact.telephone, Contact.full_address,
        Contact.default, Contact.campus_branch
    ]
    try:
        datas = Contact.select(*need).where(
            Contact.user_id == current_user.id).order_by(Contact.id.asc()).execute()
    except Exception as e:
        return make_response_json(500, f"发生如下错误 {repr(e)}")
    else:
        data = list()
        for i in datas:
            data.append(i.__data__)
        if len(data) == 0:
            return make_response_json(404, "该用户未设置任何联系地址")
    return make_response_json(200, "获取成功", data)


@api_blue.route("/generate_order", methods=["POST"])
def generate_order():
    data = request.get_json()
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    if "item_id" not in data:
        return make_response_json(400, "请求格式不对")
    try:
        data["item_id"] = int(data["item_id"])
        p = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    if p.shelved_num == 0:
        return make_response_json(404, "您请求的物品暂无库存")
    url = {"url": url_for('order.generate', item_id=data["item_id"])}
    return make_response_json(200, "跳转到订单生成页面", data=url)


#接口order_post函数公共部分
def item_list_save(data, item_list, len):
    for t in range(len):
        item_list[t].shelved_num += data["item_info"][t]["num"]
        item_list[t].locked_num -= data["item_info"][t]["num"]
        item_list[t].save()

@api_blue.route("/order_post", methods=["POST"])
def order_post():
    res = check_user(current_user, False, True)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    if current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户被封禁中")
    '''
    data = request.get_json()
    if "item_info" not in data:
        return make_response_json(400, "请求格式不对")
    if not isinstance(data["item_info"], list):
        return make_response_json(400, "请求格式不对")
    if "contact_id" not in data:
        return make_response_json(400, "请求格式不对")
    try:
        contact_id = int(data["contact_id"])
    except Exception as e:
        return make_response_json(400, "地址未填写")
    if "note" not in data:
        return make_response_json(400, "请求格式不对")
    op, tp = None, None
    item_list = list()
    call_back, start_num = (200, None), 0
    for i in range(len(data["item_info"])):
        start_num = 0
        if "item_id" not in data["item_info"][i] or "num" not in data[
                "item_info"][i]:
            call_back = (400, "请求格式不对")
            break
        try:
            data["item_info"][i]["item_id"] = int(
                data["item_info"][i]["item_id"])
            data["item_info"][i]["num"] = int(data["item_info"][i]["num"])
            item_id = data["item_info"][i]["item_id"]
            num = data["item_info"][i]["num"]
        except Exception as e:
            call_back = (400, "请求格式不对")
            break
        if num < 0:
            call_back = (400, "请求格式不对")
            break
        try:
            item = Item.get(Item.id == item_id)
        except Exception as e:
            call_back = (404, f"请求的{item.name}不存在")
            break
        if item.shelved_num < num:
            call_back = (404, f"请求的{item.name}库存不足")
            break
        if current_user.id == item.user_id.id:
            call_back = (401, "不可与自己做生意")
            break
        if op is None:
            op = item.user_id.id
        elif item.user_id.id != op:
            call_back = (400, "订单中不允许存在多个商家")
            break
        if tp is None:
            tp = item.type
        elif tp != item.type:
            call_back = (400, "订单中不允许同时存在商品和悬赏")
            break
        try:
            item.shelved_num -= num
            item.locked_num += num
            item.save()
        except Exception as e:
            call_back = (500, f"锁定物品时发生错误 {repr(e)}")
            break
        item_list.append(item)
    if call_back[0] != 200:
        item_list_save(data, item_list, start_num)
        '''
        for t in range(start_num):
            item_list[t].shelved_num += data["item_info"][t]["num"]
            item_list[t].locked_num -= data["item_info"][t]["num"]
            item_list[t].save()
        '''
        return make_response_json(call_back[0], call_back[1])
    try:
        contact = Contact.get(Contact.id == contact_id)
    except Exception as e:
        item_list_save(data, item_list, len(data["item_info"]))
        '''
        for t in range(len(data["item_info"])):
            item_list[t].shelved_num += data["item_info"][t]["num"]
            item_list[t].locked_num -= data["item_info"][t]["num"]
            item_list[t].save()
        '''
        return make_response_json(404, "不存在的地址信息")
    order_data = dict()
    order_data["user_id"] = current_user.id
    order_data["default"] = contact.default
    order_data["name"] = contact.name
    order_data["telephone"] = contact.telephone
    order_data["full_address"] = contact.full_address
    order_data["campus_branch"] = contact.campus_branch
    order_data["state"] = Order_state.Normal.value
    order_data["note"] = data["note"]
    order_data["create_time"] = datetime.now()
    order_data["payment"] = 0
    for i in range(len(item_list)):
        order_data[
            "payment"] += data["item_info"][i]["num"] * item_list[i].price
    try:
        od = Order.create(**order_data)
    except Exception as e:
        item_list_save(data, item_list, len(data["item_info"]))
        '''
        for t in range(len(data["item_info"])):
            item_list[t].shelved_num += data["item_info"][t]["num"]
            item_list[t].locked_num -= data["item_info"][t]["num"]
            item_list[t].save()
        '''
        return make_response_json(500, f"Order存储错误 {repr(e)}")
    try:
        od_st_it = Order_State_Item.create(order_id=od.id)
    except Exception as e:
        item_list_save(data, item_list, len(data["item_info"]))
        '''
        for t in range(len(data["item_info"])):
            item_list[t].shelved_num += data["item_info"][t]["num"]
            item_list[t].locked_num -= data["item_info"][t]["num"]
            item_list[t].save()
        '''
        od.delete_instance()
        return make_response_json(500, f"Order_State_Item 存储错误 {repr(e)}")
    od_it_list = list()
    for i in range(len(item_list)):
        try:
            od_it = Order_Item.create(order_id=od.id,
                                      quantity=num,
                                      price=item_list[i].price,
                                      item_id=item_list[i].id)
        except Exception as e:
            item_list_save(data, item_list, len(data["item_info"]))
            '''
            for t in range(len(data["item_info"])):
                item_list[t].shelved_num += data["item_info"][t]["num"]
                item_list[t].locked_num -= data["item_info"][t]["num"]
                item_list[t].save()
            '''
            for j in od_it_list:
                j.delete_instance()
            od_st_it.delete_instance()
            od.delete_instance()
            return make_response_json(500, f"订单详情存储时出错 {repr(e)}")
        od_it_list.append(od_it)
    if od_it.item_id.type == Item_type.Goods.value:
        send_message(SYS_ADMIN_NO, od_it.item_id.user_id.id,
                     f"已有用户购买你的商品<{od_it.item_id.name}>，请前往个人中心确认或取消订单")
    else:
        send_message(SYS_ADMIN_NO, od_it.item_id.user_id.id,
                     f"已有用户接取你的悬赏<{od_it.item_id.name}>，请前往个人中心确认或取消订单")
    return make_response_json(201, "订单生成成功，请等待商家确认", data={"order_id": od.id})


# /adress拆为三个函数
@api_blue.route("/address", methods=["POST"])
def address_post():
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = request.get_json()
    temp = [None for i in range(len(data))]

    has_default, num = False, 0
    old_default = None
    for i, j in enumerate(data):
        for k in j:
            if isinstance(j[k],str) and len(j[k]) == 0:
                return make_response_json(400,"不允许提交空参数")
        if "campus_branch" in j:
            if j["campus_branch"] not in User_Campus_state._value2member_map_:
                return make_response_json(400, "校区填写错误")
        j["user_id"] = current_user.id
        if "default" in j and j["default"]:
            if not has_default:
                has_default, num = True, i
            else:
                data[num]["default"] = False
                num = i
    try:
        old_default = Contact.get(Contact.default == True,
                                    Contact.user_id == current_user.id)
    except Exception as e:
        if not has_default:
            data[-1]["default"] = True
    else:
        if has_default:
            old_default.default = False
            old_default.save()
    for i, j in enumerate(data):
        try:
            temp[i] = Contact.create(**j)
        except Exception as e:
            for t in range(i):
                temp[t].delete_instance()
            if old_default is not None:
                old_default.default = True
                old_default.save()
            return make_response_json(500, f"存储时出现错误 {repr(e)}")

    return make_response_json(200, "完成")

@api_blue.route("/address", methods=["PUT"])
def address_put():
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = request.get_json()
    temp = [None for i in range(len(data))]
    for i, j in enumerate(data):
        # j["id"] = j["contact_id"]
        # j.pop("contact_id")
        for k in j:
            if isinstance(j[k],str) and len(j[k]) == 0:
                return make_response_json(400,"不允许提交空参数")
        if "campus_branch" in j:
            if j["campus_branch"] not in User_Campus_state._value2member_map_:
                return make_response_json(400, "校区填写错误")
        try:
            # j["id"] = j["contact_id"]
            # j.pop("contact_id")
            temp[i] = Contact.get(Contact.id == int(j["id"]))
        except Exception as e:
            return make_response_json(401, "不存在的联络地址")
        else:
            if temp[i].user_id.id != current_user.id:
                return make_response_json(401, "不可修改其他用户的联络地址")
    #update_data = list(range(len(data)))
    update_data = copy.deepcopy(temp)
    has_default, num = False, 0
    for i, j in enumerate(data):
        if "default" in j and j["default"]:
            if not has_default:
                    has_default, num = True, i
            else:
                data[num]["default"] = False
                num = i
    old_default = None
    try:
        old_default = Contact.get(Contact.default == True,
                                    Contact.user_id == current_user.id)
    except Exception as e:
        if not has_default:
            temp[-1].default = True
    else:
        if has_default:
            if old_default not in temp:
                old_default.default = False
                old_default.save()
        else:
            if old_default in temp:
                return make_response_json(400, "至少要保留一个默认地址")
    for i in range(len(temp)):
        try:
            for j in data[i]:
                if j in update_data[i].__data__:
                    exec(f"""if update_data[{i}].{j} != data[{i}]["{j}"]:
    update_data[{i}].{j} = data[{i}]["{j}"]
                        """)
                    #new_data[j] = data[i][j]
            #update_data[i] = Contact(**new_data)
            update_data[i].save()
        except Exception as e:
            for t in range(i):
                temp[i].save()
            if old_default is not None:
                old_default.default = True
                old_default.save()
            return make_response_json(500, f"存储错误 {repr(e)}")
    
    return make_response_json(200, "完成")

@api_blue.route("/address", methods=["DELETE"])
def address_delete():
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = request.get_json()
    temp = [None for i in range(len(data))]
    data = list(set(map(lambda x: x["contact_id"], data)))
    for i, j in enumerate(data):
        try:
            temp[i] = Contact.get(Contact.id == int(j))
        except Exception as e:
            return make_response_json(401, "不存在的联络地址")
        else:
            if temp[i].user_id.id != current_user.id:
                return make_response_json(401, "不可删除其他用户的联络地址")
    delete_default = False
    for i, j in enumerate(temp):
        try:
            j.delete_instance()
        except Exception as e:
            for t in range(i):
                temp[t].save()
            return make_response_json(500, f"发生错误 {repr(e)}")
        else:
            if j.default:
                delete_default = True
    if delete_default:
        try:
            datas = Contact.select().where(
                Contact.user_id == current_user.id).order_by(
                    Contact.id.desc()).execute()
        except Exception as e:
            print(repr(e))
        else:
            if len(datas) > 0:
                datas[0].default = True
                datas[0].save()

    return make_response_json(200, "完成")

'''
@api_blue.route("/address", methods=["POST", "PUT", "DELETE"])
def address():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    temp = [None for i in range(len(data))]
    if request.method == "DELETE":
        data = list(set(map(lambda x: x["contact_id"], data)))
        for i, j in enumerate(data):
            try:
                temp[i] = Contact.get(Contact.id == int(j))
            except Exception as e:
                return make_response_json(401, "不存在的联络地址")
            else:
                if temp[i].user_id.id != current_user.id:
                    return make_response_json(401, "不可删除其他用户的联络地址")
        delete_default = False
        for i, j in enumerate(temp):
            try:
                j.delete_instance()
            except Exception as e:
                for t in range(i):
                    temp[t].save()
                return make_response_json(500, f"发生错误 {repr(e)}")
            else:
                if j.default:
                    delete_default = True
        if delete_default:
            try:
                datas = Contact.select().where(
                    Contact.user_id == current_user.id).order_by(
                        Contact.id.desc()).execute()
            except Exception as e:
                print(repr(e))
            else:
                if len(datas) > 0:
                    datas[0].default = True
                    datas[0].save()
    elif request.method == "PUT":
        for i, j in enumerate(data):
            # j["id"] = j["contact_id"]
            # j.pop("contact_id")
            for k in j:
                if isinstance(j[k],str) and len(j[k]) == 0:
                    return make_response_json(400,"不允许提交空参数")
            if "campus_branch" in j:
                if j["campus_branch"] not in User_Campus_state._value2member_map_:
                    return make_response_json(400, "校区填写错误")
            try:
                # j["id"] = j["contact_id"]
                # j.pop("contact_id")
                temp[i] = Contact.get(Contact.id == int(j["id"]))
            except Exception as e:
                return make_response_json(401, "不存在的联络地址")
            else:
                if temp[i].user_id.id != current_user.id:
                    return make_response_json(401, "不可修改其他用户的联络地址")
        #update_data = list(range(len(data)))
        update_data = copy.deepcopy(temp)
        has_default, num = False, 0
        for i, j in enumerate(data):
            if "default" in j and j["default"]:
                if not has_default:
                    has_default, num = True, i
                else:
                    data[num]["default"] = False
                    num = i
        old_default = None
        try:
            old_default = Contact.get(Contact.default == True,
                                      Contact.user_id == current_user.id)
        except Exception as e:
            if not has_default:
                temp[-1].default = True
        else:
            if has_default:
                if old_default not in temp:
                    old_default.default = False
                    old_default.save()
            else:
                if old_default in temp:
                    return make_response_json(400, "至少要保留一个默认地址")
        for i in range(len(temp)):
            try:
                for j in data[i]:
                    if j in update_data[i].__data__:
                        exec(f"""if update_data[{i}].{j} != data[{i}]["{j}"]:
    update_data[{i}].{j} = data[{i}]["{j}"]
                        """)
                        #new_data[j] = data[i][j]
                #update_data[i] = Contact(**new_data)
                update_data[i].save()
            except Exception as e:
                for t in range(i):
                    temp[i].save()
                if old_default is not None:
                    old_default.default = True
                    old_default.save()
                return make_response_json(500, f"存储错误 {repr(e)}")
    else:
        has_default, num = False, 0
        old_default = None
        for i, j in enumerate(data):
            for k in j:
                if isinstance(j[k],str) and len(j[k]) == 0:
                    return make_response_json(400,"不允许提交空参数")
            if "campus_branch" in j:
                if j["campus_branch"] not in User_Campus_state._value2member_map_:
                    return make_response_json(400, "校区填写错误")
            j["user_id"] = current_user.id
            if "default" in j and j["default"]:
                if not has_default:
                    has_default, num = True, i
                else:
                    data[num]["default"] = False
                    num = i
        try:
            old_default = Contact.get(Contact.default == True,
                                      Contact.user_id == current_user.id)
        except Exception as e:
            if not has_default:
                data[-1]["default"] = True
        else:
            if has_default:
                old_default.default = False
                old_default.save()
        for i, j in enumerate(data):
            try:
                temp[i] = Contact.create(**j)
            except Exception as e:
                for t in range(i):
                    temp[t].delete_instance()
                if old_default is not None:
                    old_default.default = True
                    old_default.save()
                return make_response_json(500, f"存储时出现错误 {repr(e)}")

    return make_response_json(200, "完成")
'''

@api_blue.route("/order_evaluate", methods=["POST"])
def order_evaluate():
    res = check_user(current_user)
    if res[0] == -1:
        return res[1]
    '''
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    '''
    data = request.get_json()
    if "feedback_content" not in data:
        return make_response_json(400, "请求格式不对")
    if len(data["feedback_content"])>Review.feedback_content.max_length:
        return make_response_json(400,"评论超过字数限制,请限制在100字以内")
    try:
        order_id = int(data["order_id"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        order = Order.get(Order.id == order_id)
    except Exception as e:
        return make_response_json(404, "请求订单不存在")
    if order.state != Order_state.End.value:
        return make_response_json(400, "不可评价未完成订单")
    try:
        order_state_item = Order_State_Item.get(
            Order_State_Item.order_id == order_id)
    except Exception as e:
        return make_response_json(500, f"查询过程出现问题 {repr(e)}")
    if order.user_id.id == current_user.id:
        if order_state_item.user_review_id == None:  #不存在就加
            try:
                review = Review.create(
                    user_id=current_user.id,
                    publish_time=datetime.now(),
                    feedback_content=data["feedback_content"])
            except Exception as e:
                return make_response_json(500, f"存储过程出现问题 {repr(e)}")
            order_state_item.user_review_id = review
        else:  #存在就返回error
            return make_response_json(401, f"您已评价过该订单")
    else:
        try:
            od_it = Order_Item.get(Order_Item.order_id == order_id)
        except Exception as e:
            review.delete_instance()
            return make_response_json(500, f"查询过程出现问题 {repr(e)}")
        if od_it.item_id.user_id.id == current_user.id:
            if order_state_item.op_user_review_id == None:
                try:
                    review = Review.create(
                        user_id=current_user.id,
                        publish_time=datetime.now(),
                        feedback_content=data["feedback_content"])
                except Exception as e:
                    return make_response_json(500, f"存储过程出现问题 {repr(e)}")
                order_state_item.op_user_review_id = review
            else:
                return make_response_json(401, f"您已评价过该订单")
        else:
            return make_response_json(401, "无权评论此订单")
    order_state_item.save()
    return make_response_json(200, "评价完成", {"url": url_for('user.order')})


"""
@api_blue.route("/test",methods=["GET"])
def test():
    a = Contact.select().execute()
    b = [Contact.get(Contact.id == i.id) for i in a]
    c = Contact.get(Contact.user_id==1951705)
    print(c in b)
    for i in b:
        if i.user_id.id==1951705:
            i.default = not i.default
    print(c in b)
    return make_response_json()
"""