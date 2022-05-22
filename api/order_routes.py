#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_state


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

    order_user_id = order.user_id.id
    order_op_user_id = order.op_user_id.id
    if current_user.state == User_state.Admin.value:  #管理员
        order.state = req_state
        order.save()
        return make_response_json(200, "操作成功")

    elif current_user.id != order_user_id and current_user.id != order_op_user_id:  #不是订单双方
        return make_response_json(401, "当前用户不是订单双方之一，未授权")
    elif req_state == order.state:  #要修改的状态和数据库内订单状态重复了，改不改都一样，直接返回成功
        return make_response_json(200, "操作成功")
    elif order.state == Order_state.End.value or order.state == Order_state.Close.value:  #订单处于完成或关闭的状态
        return make_response_json(401, "当前订单已完成或取消，操作失败，当前用户未授权")

    elif current_user.id == order_user_id:  #当前用户是订单发起者
        if req_state == Order_state.End.value:  #想完成订单
            if order.state == Order_state.Confirm.value:  #已确认、待完成
                try:
                    _order_item = Order_Item.get(
                        Order_Item.order_id == order)  #根据order找订单明细
                except:
                    return make_response_json(404, "没有找到此订单明细")
                if _order_item.item_id.type == Item_type.Goods.value:  #发起者只能完成商品订单
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
            order.state = Order_state.Close.value
            order.save()
            return make_response_json(200, "操作成功")

        else:  #想确认订单或取消确认订单 即确认或者取消确认两种状态互转
            try:
                _order_state_item = Order_State_Item.get(
                    Order_State_Item.order_id == order)  #根据order找状态明细
            except Exception as e:
                return make_response_json(404, f"没有找到此订单状态明细")
            if req_state == Order_state.Confirm.value:  #或者确认订单
                _order_state_item.user_confirm = True  #确认订单
                _order_state_item.save()
                if _order_state_item.op_user_confirm == True:  #对方也已经确认了
                    order.state = Order_state.Confirm.value
                    order.save()
                return make_response_json(200, "操作成功")
            elif req_state == Order_state.Normal.value:  #取消确认订单（让订单从本方已确认转为本方未确认）
                _order_state_item.user_confirm = False  #取消确认订单
                _order_state_item.save()
                order.state = Order_state.Normal.value
                order.save()
                return make_response_json(200, "操作成功")
            else:
                return make_response_json(500, "req_state订单状态错误！")

    elif current_user.id == order_op_user_id:  #当前用户是物品发布者（非订单发起者）
        if req_state == Order_state.End.value:  #想完成订单
            if order.state == Order_state.Confirm.value:  #已确认、待完成
                try:
                    _order_item = Order_Item.get(
                        Order_Item.order_id == order)  #根据order找订单明细
                except:
                    return make_response_json(404, "没有找到此订单明细")
                if _order_item.item_id.type == Item_type.Want.value:  #非订单发起者只能完成悬赏订单
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
            order.state = Order_state.Close.value
            order.save()
            return make_response_json(200, "操作成功")

        else:  #想确认订单或取消确认订单 即确认或者取消确认两种状态互转
            try:
                _order_state_item = Order_State_Item.get(
                    Order_State_Item.order_id == order)  #根据order找状态明细
            except Exception as e:
                return make_response_json(404, f"没有找到此订单状态明细")
            if req_state == Order_state.Confirm.value:  #或者确认订单
                _order_state_item.op_user_confirm = True  #确认订单
                _order_state_item.save()
                if _order_state_item.user_confirm == True:  #订单发布者也已经确认了
                    order.state = Order_state.Confirm.value
                    order.save()
                return make_response_json(200, "操作成功")
            elif req_state == Order_state.Normal.value:  #取消确认订单（让订单从本方已确认转为本方未确认）
                _order_state_item.op_user_confirm = False  #取消确认订单
                _order_state_item.save()
                order.state = Order_state.Normal.value
                order.save()
                return make_response_json(200, "操作成功")
            else:
                return make_response_json(500, "数据库中订单状态错误！")
