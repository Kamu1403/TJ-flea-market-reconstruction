#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state

@api_blue.route('/get_item_info', methods=['GET'])
def get_item_info():
    item_id = int(request.args.get('item_id'))
    res = copy.deepcopy(default_res)
    try:
        it = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(404, "未找到此商品")
    else:
        res['statusCode'] = 200
        res['success'] = True
        res['message'] = "已找到商品信息"
        dic = it.__data__
        dic.pop('id')
        dic.pop('locked_num')
        res['data'] = dic
        dic['publish_time'] = str(dic['publish_time'])
        dic['price'] = float(dic['price'])
        if not current_user.is_authenticated:
            isAdmin = False
            isPub = False
        else:
            isAdmin = (current_user.state == User_state.Admin.value)
            isPub = (it.user_id.id == current_user.id)
        res["isAdmin"] = isAdmin
        res["isPub"] = isPub
    return make_response(jsonify(res))

@api_blue.route('/search', methods=['POST'])
def get_search():
    search_type = int(request.form.get("search_type"))
    if search_type != Item_type.Goods.value and search_type != Item_type.Want.value:
        return make_response_json(400, "搜索类型仅能指定商品或悬赏")

    key_word = request.form.get("key_word")
    order_type = request.form.get("order_type")
    data = []

    #get_data = Item.select().where().exectue()
    if order_type == "time":
        orderWay = (Item.publish_time.desc(), )
    elif order_type == "price":
        orderWay = (Item.price.asc(), )
    else:
        orderWay = (Item.publish_time.desc(), )  # 改：默认其实为相似度

    need = (Item.id, Item.name, Item.user_id, Item.publish_time, Item.price)
    select_need = [Item.name.contains(key_word), Item.type == search_type]
    try:
        start_time = request.form.get("start_time")
        if start_time != "" and start_time is not None:
            start_time = datetime.strptime(start_time, "%Y-%m-%d")
            select_need.append(Item.publish_time >= start_time)
        end_time = request.form.get("end_time")
        if end_time != "" and end_time is not None:
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
            select_need.append(Item.publish_time <= end_time)
    except Exception as e:
        print(e)
        return make_response_json(400, '时间格式错误,应为年-月-日格式')
    else:
        get_data = Item.select(*need).where(*select_need).order_by(
            *orderWay).execute()
        for i in get_data:
            j = i.__data__
            j['price'] = float(j['price'])
            j['publish_time'] = str(j['publish_time'])
            data.append(j)
        return make_response_json(200, "搜索结果如下", data)


@api_blue.route("/change_item_status", methods=["PUT"])
def change_item_status():
    if not current_user.is_authenticated:
        return make_response_json(400, "当前用户未登录")
    data = json.loads(request.get_json())
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if item.type == data["state"]:
            return make_response_json(400, "商品当前状态和希望更改的状态相同")
        else:
            if current_user.state == User_state.Admin.value:
                return make_response_json(200, "操作成功")
            elif current_user.state == User_state.Under_ban.value:
                return make_response_json(400, "您当前已被封号,请联系管理员解封")
            else:
                if current_user.id != item.user_id_id:
                    return make_response_json(400, "不可改变其他人的商品状态")
                else:
                    if data["state"] == Item_state.Freeze.value:
                        return make_response_json(400, "权限不足")
                    else:
                        return make_response_json(200, "操作成功")
