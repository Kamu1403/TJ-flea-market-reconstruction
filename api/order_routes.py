#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue

MINUS_SCORE = 5  #取消一个已经确认了的订单，扣五分


@api_blue.route("/change_order_status", methods=["PUT"])
def change_order_status():
    req = request.get_json()

    req_state = int(req['state'])
    if req_state not in Order_state._value2member_map_:
        return make_response_json(400, "请求格式不对")

    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    elif current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户已被封禁")

    try:
        order = Order.get(Order.id == req['order_id'])
    except Exception as e:
        return make_response_json(404, f"没有找到此订单")
    try:
        _order_item = Order_Item.get(
            Order_Item.order_id == order)  #根据order找订单明细
    except:
        return make_response_json(404, "没有找到此订单明细")

    order_user_id = order.user_id.id
    order_op_user_id = _order_item.item_id.user_id
    if current_user.state == User_state.Admin.value:  #管理员,无限权力
        order.state = req_state
        if req_state == Order_state.Close.value:  #取消订单
            _order_item.item_id.locked_num -= _order_item.quantity
            _order_item.item_id.shelved_num += _order_item.quantity
            _order_item.item_id.save()
        if req_state == Order_state.End.value:  #完成订单
            _order_item.item_id.locked_num -= _order_item.quantity
            _order_item.item_id.save()
        order.save()
        return make_response_json(200, "操作成功")
    elif req_state == Order_state.Normal.value:  #非管理员不允许设为初始状态
        return make_response_json(400, "请求格式不对")
    elif current_user.id != order_user_id and current_user.id != order_op_user_id:  #不是订单双方
        return make_response_json(401, "当前用户不是订单双方之一，未授权")
    elif req_state == order.state:  #要修改的状态和数据库内订单状态重复了，改不改都一样，直接返回成功
        return make_response_json(400, "操作过于频繁")
    elif order.state == Order_state.End.value or order.state == Order_state.Close.value:  #订单处于完成或关闭的状态
        return make_response_json(401, "当前订单已完成或取消，操作失败，当前用户未授权")

    elif current_user.id == order_user_id:  #当前用户是订单发起者
        if req_state == Order_state.End.value:  #想完成订单
            if order.state == Order_state.Confirm.value:  #已确认、待完成
                if _order_item.item_id.type == Item_type.Goods.value:  #发起者只能完成商品订单
                    _order_item.item_id.locked_num -= _order_item.quantity
                    _order_item.item_id.save()
                    order.state = Order_state.End.value
                    order.save()
                    return make_response_json(200, "操作成功")
                else:
                    return make_response_json(401, "悬赏订单只能由悬赏发布者完成，当前用户未授权")
            elif order.state == Order_state.Normal.value:  #还没确认
                return make_response_json(401, "当前用户未授权，请等待订单确认后再点击完成订单")
            else:
                return make_response_json(500, "数据库中订单状态错误！")

        elif req_state == Order_state.Close.value:  #想取消订单
            if order.state == Order_state.Confirm.value:  #已经确认过的，要扣除信誉分 5 分
                order.user_id.score -= MINUS_SCORE
                order.user_id.save()
            _order_item.item_id.locked_num -= _order_item.quantity
            _order_item.item_id.shelved_num += _order_item.quantity
            _order_item.item_id.save()
            order.state = Order_state.Close.value
            order.save()
            return make_response_json(200, "操作成功")

        elif req_state == Order_state.Confirm.value:  #想确认订单
            return make_response_json(401, "未授权，您无需确认，请等待对方确认")
        else:
            return make_response_json(500, "req_state订单状态错误！")

    elif current_user.id == order_op_user_id:  #当前用户是物品发布者（非订单发起者）
        if req_state == Order_state.End.value:  #想完成订单
            if order.state == Order_state.Confirm.value:  #已确认、待完成
                if _order_item.item_id.type == Item_type.Want.value:  #非订单发起者只能完成悬赏订单
                    _order_item.item_id.locked_num -= _order_item.quantity
                    _order_item.item_id.save()
                    order.state = Order_state.End.value
                    order.save()
                    return make_response_json(200, "操作成功")
                else:
                    return make_response_json(401, "商品订单只能由购买者完成，当前用户未授权")
            elif order.state == Order_state.Normal.value:  #还没确认
                return make_response_json(401, "当前用户未授权，请等待订单确认后再点击完成订单")
            else:
                return make_response_json(500, "数据库中订单状态错误！")

        elif req_state == Order_state.Close.value:  #想取消订单
            if order.state == Order_state.Confirm.value:  #已经确认过的，要扣除信誉分 5 分
                order_op_user_id.score -= MINUS_SCORE
                order_op_user_id.save()
            _order_item.item_id.locked_num -= _order_item.quantity
            _order_item.item_id.shelved_num += _order_item.quantity
            _order_item.item_id.save()
            order.state = Order_state.Close.value
            order.save()
            return make_response_json(200, "操作成功")

        elif req_state == Order_state.Confirm.value:  #想确认订单
            order.state = Order_state.Confirm.value
            order.save()
            return make_response_json(200, "操作成功")
        else:
            return make_response_json(500, "req_state订单状态错误！")


@api_blue.route("/get_item_id_by_order", methods=["GET"])
def get_item_id_by_order():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = dict(request.args)
    try:
        order_id = int(data['order_id'])
    except:
        return make_response_json(400, "请求格式不对")
    need = [Order_Item.quantity, Order_Item.item_id]
    try:
        datas = Order_Item.select(*need).where(Order_Item.order_id == order_id)
        order_user_id = Order.get(Order.id == order_id).user_id.id
    except Exception as e:
        return make_response_json(500, f"发生如下错误\n{repr(e)}")
    else:
        if datas.count() <= 0:
            return make_response_json(404, "未找到该订单明细")
        if datas[0].item_id.user_id.id != current_user.id \
           and order_user_id != current_user.id \
           and current_user.state != User_state.Admin.value:
            return make_response_json(401, "无此权限")

        res = list()
        for i in datas:
            tep = {"quantity": i.quantity, "item_id": i.item_id.id}
            res.append(tep)
        return make_response_json(200, "获取成功", res)