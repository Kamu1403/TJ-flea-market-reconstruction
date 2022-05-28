#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from order.models import Contact
from datetime import date, timedelta


@api_blue.route("/get_order", methods=["GET"])
def get_order():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = dict(request.args)
    need = [(Order.user_id == current_user.id) |
            (Order.op_user_id == current_user.id)]
    ordered_num = False
    if "max_num" in data:
        try:
            data["max_num"] = int(data["max_num"])
        except Exception as e:
            return make_response_json(400, "请求格式错误")
        else:
            ordered_num = True
    if "range" in data:
        try:
            data["range"] = int(data["range"])
        except Exception as e:
            return make_response_json(400, "请求格式错误")
        else:
            td = timedelta(days=data["range"])
            last_time = date.today() - td
            need.append(Order.create_time >= last_time)
    try:
        need_od = Order.select().where(*need).order_by(
            Order.create_time.desc()).execute()
    except Exception as e:
        return make_response_json(500, f"查询发生错误 {repr(e)}")
    else:
        datas = {
            "wait_confirmation_op": list(),
            "wait_confirmation_self": list(),
            "others": list()
        }
        for i in need_od:
            j = i.__data__
            if j["state"] == Order_state.Close.value or j[
                    "state"] == Order_state.End.value:
                if ordered_num and len(datas["others"]) == data["max_num"]:
                    continue
                datas["others"].append(j)
            elif j["state"] == Order_state.Normal.value:
                if j["user_id"] == current_user.id:
                    if ordered_num and len(datas["others"]) == data["max_num"]:
                        continue
                    datas["wait_confirmation_op"].append(j)
                else:
                    if ordered_num and len(datas["others"]) == data["max_num"]:
                        continue
                    datas["wait_confirmation_self"].append(j)
            else:
                if j["user_id"] == current_user.id:
                    if ordered_num and len(datas["others"]) == data["max_num"]:
                        continue
                    datas["wait_confirmation_self"].append(j)
                else:
                    if ordered_num and len(datas["others"]) == data["max_num"]:
                        continue
                    datas["wait_confirmation_op"].append(j)
    return make_response_json(200, "返回订单", datas)


@api_blue.route("/get_address", methods=['GET'])
def get_address():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    elif current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户已被封禁")
    need = [
        Contact.name, Contact.telephone, Contact.full_address, Contact.default,
        Contact.campus_branch
    ]
    try:
        datas = Contact.select(*need).where(
            Contact.user_id == current_user.id).execute()
    except Exception as e:
        return make_response_json(500, f"发生如下错误\n{repr(e)}")
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
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
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


@api_blue.route("/order_post", methods=["POST"])
def order_post():

    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    if current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户被封禁中")
    data = request.get_json()
    if "item_info" not in data:
        return make_response_json(400,"请求格式不对")
    if not isinstance(data["item_info"],list):
        return make_response_json(400,"请求格式不对")
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(400, "不存在此款物品")
    if item.shelved_num < data["num"]:
        return make_response_json(401, "物品库存不足")
    if current_user.id == item.user_id.id:
        return make_response_json(401, "不可自己和自己做生意")
    try:
        contact = Contact.get(Contact.id == data["contact_id"])
    except Exception as e:
        return make_response_json(400, "您指定的联系方式不存在")
    try:
        op_contact = Contact.get(Contact.user_id == item.user_id)
    except Exception as e:
        return make_response_json(400, "对方未存储联系方式")
    try:
        order_data = dict()
        order_data["user_id"] = item.user_id.id
        order_data["op_user_id"] = current_user.id
        order_data["contact_id"] = op_contact.id
        order_data["op_contact_id"] = data["contact_id"]
        order_data["note"] = data["note"]
        order_data["payment"] = float(item.price) * data["num"]
        od = Order.create(**order_data)
    except Exception as e:
        return make_response_json(500, f"存储错误 {repr(e)}")
    else:
        try:
            od_it = Order_Item.create(order_id=od.id,
                                      quantity=data["num"],
                                      item_id=item.id)
        except Exception as e:
            od.delete_instance()
            return make_response_json(500, f"存储错误 {repr(e)}")
        else:
            try:
                od_st_it = Order_State_Item.create(order_id=od.id)
            except Exception as e:
                od_it.delete_instance()
                od.delete_instance()
                return make_response_json(500, f"存储错误 {repr(e)}")
        try:
            item.locked_num += data["num"]
            item.shelved_num -= data["num"]
            item.save()
        except Exception as e:
            od_st_it.delete_instance()
            od_it.delete_instance()
            od.delete_instance()
            return make_response_json(500, f"存储错误 {repr(e)}")
    return make_response_json(200,
                              "订单生成成功，请等待商家确认",
                              data=url_for("order.manage"))


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
                    p = Contact.get(Contact.id == datas[0].id)
                    p.default = True
                    p.save()
    elif request.method == "PUT":
        for i, j in enumerate(data):
            try:
                temp[i] = Contact.get(Contact.id == int(j["contact_id"]))
            except Exception as e:
                return make_response_json(401, "不存在的联络地址")
            else:
                if temp[i].user_id.id != current_user.id:
                    return make_response_json(401, "不可修改其他用户的联络地址")
        update_data = list(range(len(data)))
        has_default, num = False, 0
        for i, j in enumerate(data):
            if "default" in j and j["default"]:
                if not has_default:
                    has_default, num = True, i
                else:
                    data[num]["default"] = False
                    num = i
        old_default = None
        if has_default:
            try:
                old_default = Contact.get(Contact.default == True)
            except Exception as e:
                pass
            else:
                if old_default not in temp:
                    old_default.default = False
                    old_default.save()
        for i in range(len(temp)):
            try:
                new_data = dict()
                for j in data[i]:
                    if j in dir(update_data[i]):
                        new_data[j] = data[i][j]
                update_data[i] = Contact(**new_data)
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
            j["user_id"] = current_user.id
            if "default" in j and j["default"]:
                if not has_default:
                    has_default, num = True, i
                else:
                    data[num]["default"] = False
                    num = i
        if has_default:
            try:
                old_default = Contact.get(Contact.default == True)
            except Exception as e:
                pass
            else:
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


@api_blue.route("/order_evaluate", methods=["POST"])
def order_evaluate():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    if "feedback_content" not in data:
        return make_response_json(400, "请求格式不对")
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
        review = Review.create(user_id=current_user.id,
                               publish_time=date.today(),
                               feedback_content=data["feedback_content"])
    except Exception as e:
        return make_response_json(500, f"存储过程出现问题 {repr(e)}")
    try:
        order_state_item = Order_State_Item.get(
            Order_State_Item.order_id == order_id)
    except Exception as e:
        review.delete_instance()
        return make_response_json(500, f"查询过程出现问题 {repr(e)}")
    if order.user_id.id == current_user.id:
        order_state_item.user_review_id = review
    elif order_state_item.op_user_id.id == current_user.id:
        order_state_item.op_user_review_id = review
    else:
        review.delete_instance()
        return make_response_json(500, "订单存储时出现问题")
    order_state_item.save()
    return make_response_json(200, "评价完成", {"url": url_for('order.manage')})


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