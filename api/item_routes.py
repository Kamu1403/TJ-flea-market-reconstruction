#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from item import item_blue
from admin.models import Feedback, Feedback_kind, Feedback_state
from datetime import datetime, date, timedelta
from hashlib import md5


def createPath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)


@api_blue.route("/get_item_pics", methods=['GET'])
def get_item_pics():
    data = request.get_json()
    try:
        item_id = int(data["item_id"])
    except Exception as e:
        return make_response_json(400, f"请求格式错误 {repr(e)}")
    pic_path = os.listdir(
        os.path.join(item_blue.static_folder, 'resource/item_pic/1/pic'))
    if len(pic_path):
        pic_list = list()
        for i in pic_path:
            pic_list.append(
                url_for('item.static',
                        filename=f'resource/item_pic/{item_id}/pic/{i}'))
        return make_response_json(200, "图片查找成功", data={"url": pic_list})
    else:
        return make_response_json(400, "此物品不存在")


@api_blue.route('/get_item_info', methods=['GET'])
def get_item_info():
    try:
        item_id = int(request.args.get('item_id'))
    except Exception as e:
        return make_response_json(400, "请求格式错误")
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


@api_blue.route("/get_user_item", methods=["GET"])
def get_user_item():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    try:
        kind = int(data["kind"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    if kind != Item_type.Goods.value and kind != Item_type.Want.value:
        return make_response_json(400, "请求格式不对")
    try:
        item_list = Item.select().where(Item.user_id == current_user.id,
                                        Item.type == kind).execute()
    except Exception as e:
        return make_response_json(500, f"查询错误 {repr(e)}")
    datas = list()
    for i in item_list:
        j = i.__data__
        j.pop('type')
        if current_user.state != User_state.Admin.value:
            j.pop('locked_num')
        datas.append(j)
    return make_response_json(200, "查询成功", data=datas)


@api_blue.route('/search', methods=['POST'])
def get_search():
    try:
        search_type = int(request.form.get("search_type"))
    except Exception as e:
        return make_response_json(400, "请求格式错误")
    if search_type != Item_type.Goods.value and search_type != Item_type.Want.value:
        return make_response_json(400, "搜索类型仅能指定商品或悬赏")
    key_word = request.form.get("key_word")
    order_type = request.form.get("order_type")
    data = list()

    #get_data = Item.select().where().exectue()
    if order_type == "time":
        orderWay = (Item.publish_time.desc(), )
    elif order_type == "price":
        orderWay = (Item.price.asc(), )
    else:
        orderWay = (Item.publish_time.desc(), )  # 改：默认其实为相似度

    need = (Item.id, Item.name, Item.user_id, Item.publish_time, Item.price,Item.tag)
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
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    try:
        data["item_id"] = int(data["item_id"])
        data["state"] = int(data["state"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if item.type == data["state"]:
            return make_response_json(400, "商品当前状态和希望更改的状态相同")
        else:
            if current_user.state == User_state.Admin.value:
                item.state = data["state"]
                item.save()
                return make_response_json(200, "操作成功")
            elif current_user.state == User_state.Under_ban.value:
                return make_response_json(401, "您当前已被封号,请联系管理员解封")
            else:
                if current_user.id != item.user_id.id:
                    return make_response_json(401, "不可改变其他人的商品状态")
                else:
                    if data["state"] == Item_state.Freeze.value:
                        return make_response_json(401, "权限不足")
                    else:
                        item.state = data["state"]
                        item.save()
                        return make_response_json(200, "操作成功")


@api_blue.route("/change_item_num", methods=["PUT"])
def change_item_num():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    try:
        data["item_id"] = int(data["item_id"])
        data["num"] = int(data["num"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if current_user.state == User_state.Admin.value:
            item.shelved_num = data["num"]
            item.save()
            return make_response_json(200, "操作成功")
        elif current_user.state == User_state.Under_ban.value:
            return make_response_json(401, "您当前已被封号,请联系管理员解封")
        else:
            if current_user.id != item.user_id_id:
                return make_response_json(401, "不可改变其他人的商品状态")
            else:
                if data["state"] == Item_state.Freeze.value:
                    return make_response_json(401, "权限不足")
                else:
                    item.shelved_num = data["num"]
                    item.save()
                    return make_response_json(200, "操作成功")


@api_blue.route("/change_item_data", methods=["PUT"])
def change_item_data():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = request.get_json()
    try:
        data["item_id"] = int(data["item_id"])
        if "shelved_num" in data:
            data["shelved_num"] = int(data["shelved_num"])
        if "locked_num" in data:
            data["locked_num"] = int(data["locked_num"])
        if "price" in data:
            data["price"] = float(data["price"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if current_user.state == User_state.Admin.value:
            for i in data:
                if i not in dir(item):
                    data.pop(i)
            item = Item(**data)
            item.save()
            return make_response_json(200, "操作成功")
        elif current_user.state == User_state.Under_ban.value:
            return make_response_json(401, "您当前已被封号,请联系管理员解封")
        else:
            if current_user.id != item.user_id_id:
                return make_response_json(401, "不可改变其他人的商品状态")
            else:
                if data["state"] == Item_state.Freeze.value:
                    return make_response_json(401, "权限不足")
                else:
                    for i in data:
                        if i in dir(item):
                            data.pop(i)
                    item = Item(**data)
                    item.save()
                    return make_response_json(200, "操作成功")


@api_blue.route("/post_item_info", methods=["POST"])
def post_item_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    if current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户已被封号")
    data = request.get_json()
    print(data)
    if data["price"] <= 0:
        return make_response_json(400, "物品不存在负价格")
    if data["type"] != Item_type.Goods.value and data[
            "type"] != Item_type.Want.value:
        return make_response_json(400, "仅能上传物品")
    if data["shelved_num"] <= 0:
        return make_response_json(400, "不允许发布负数个物品")
    data["user_id"] = current_user.id
    data["publish_time"] = datetime.now()
    try:
        new = Item.create(**data)
    except Exception as e:
        return make_response_json(400, f"上传失败\n{str(e)}:{repr(e)}")
    createPath(
        os.path.join(item_blue.static_folder,
                     f'resource/item_pic/{new.id}/head'))
    createPath(
        os.path.join(item_blue.static_folder,
                     f'resource/item_pic/{new.id}/pic'))
    if len(data["urls"]) == 0:
        #给一个默认图
        with open(
                url_for('item.static', filename=f'resource/default/test.jpg'),
                "rb") as f:
            g = open(
                url_for('item.static',
                        filename=f'resource/item_pic/{new.id}/head/0.jpg'),
                "wb")
            g.write(f.read())
            g.close()
            h = open(
                url_for('item.static',
                        filename=f'resource/item_pic/{new.id}/pic/0.jpg'),
                "wb")
            h.write(f.read())
            h.close()
    else:
        head_pics = [i["MD5"] for i in data["urls"] if i["is_cover_pic"]]
        if len(head_pics) == 0:
            head_pic = data["urls"][0]["MD5"]
        elif len(head_pics) > 1:
            new.delete_instance()
            return make_response_json(400, "仅能选定一张头图")
        else:
            head_pic = head_pics[0]
        with open(
                url_for(
                    'item.static',
                    filename=f'resource/temp/{current_user.id}/{head_pic}.jpg'
                ), "rb") as f:
            g = open(
                url_for('item.static',
                        filename=f'resource/item_pic/{new.id}/head/0.jpg'),
                "wb")
            g.write(f.read())
            g.close()
        for i, j in enumerate(data["urls"]):
            with open(
                    url_for('item.static',
                            filename=
                            f'resource/temp/{current_user.id}/{j["MD5"]}.jpg'),
                    "rb") as f:
                g = open(
                    url_for(
                        'item.static',
                        filename=f'resource/item_pic/{new.id}/pic/{i}.jpg'),
                    "wb")
                g.write(f.read())
                g.close()
        #将所有的图片转到用户对应文件夹
    return make_response_json(200, "上传成功")


@api_blue.route("/post_item_pic", methods=["POST"])
def post_item_pic():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    try:
        data = request.files["file"]
        file_byte = data.read()
        md5code = md5(file_byte).hexdigest()
        createPath(
            os.path.join(item_blue.static_folder,
                         f'resource/temp/{current_user.id}/'))
        with open(
                url_for(
                    'item.static',
                    filename=f'resource/temp/{current_user.id}/{md5code}.jpg'),
                "wb") as f:
            f.write(file_byte)
    except Exception as e:
        return make_response_json(400, f"上传失败\n{str(e)}{repr(e)}")
    return make_response_json(200, "上传图片成功", {"str": md5code})


@api_blue.route("/add_favor", methods=["POST"])
def add_favor():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    req = request.get_json()["item_id_list"]

    tep = Item.select().where(Item.id << req)  #在一个列表中查询
    if tep.count() != len(req):  #长度对不上
        return make_response_json(404, "不存在对应物品")
    try:
        repeat = False
        for i in req:
            tep = Favor.select().where((Favor.user_id == current_user.id)
                                       & (Favor.item_id == i))
            if tep.count() > 0:
                repeat = True
            else:
                Favor.insert(user_id=current_user.id, item_id=i).execute()
        if repeat == True:
            return make_response_json(400, "重复添加")
        return make_response_json(201, "添加成功")
    except Exception as e:
        return make_response_json(500, f"发生错误 {repr(e)}")


@api_blue.route("/delete_favor", methods=["DELETE"])
def item_delete_favor():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    req = request.get_json()["item_id_list"]

    #tep = Item.select().where(Item.id << req)  #在一个列表中查询
    #if tep.count() != len(req):  #长度对不上
    #    return make_response_json(404, "不存在对应物品")
    try:
        NotFound = False
        for i in req:
            tep = Favor.select().where((Favor.user_id == current_user.id)
                                       & (Favor.item_id == i))

            if tep.count() <= 0:
                NotFound = True
            else:
                Favor.delete().where((Favor.user_id == current_user.id)
                                     & (Favor.item_id == i)).execute()
        if NotFound == True:
            return make_response_json(404, "不存在对应的收藏")
        return make_response_json(200, "删除成功")
    except Exception as e:
        return make_response_json(500, f"发生错误 {repr(e)}")


@api_blue.route("/get_favor", methods=["GET"])
def item_get_favor():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    tep = Favor.select().where(Favor.user_id == current_user.id).execute()
    data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        res['collect_time'] = str(i.collect_time)
        data.append(res)
    return make_response_json(200, "操作成功", data)


@api_blue.route("/get_history", methods=["GET"])
def get_history():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    tep = History.select().where(History.user_id == current_user.id).execute()
    data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        res['visit_time'] = str(i.visit_time)
        data.append(res)
    return make_response_json(200, "操作成功", data)


@api_blue.route("/report_item", methods=["POST"])
def report_item():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户还未登陆")
    data = request.get_json()
    if "reason" not in data:
        return make_response_json(400, "请求格式不对")
    try:
        item_id = int(data["item_id"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        item = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(404, "不存在的物品")
    data["reason"] = "物品id:{} 物品名称:{} ".format(item_id,
                                               item.name) + data["reason"]
    try:
        feedback_data = {
            "user_id": current_user.id,
            "publish_time": date.today(),
            "kind": Feedback_kind.Item.value
        }
        feedback_data["reply_content"] = data["reason"]
        feedback = Feedback.create(**feedback_data)
    except Exception as e:
        return make_response_json(500, f"存储出现问题 {repr(e)}")
    return make_response_json(200, "举报完成,请等待管理员处理...")


@api_blue.route("/item_to_show", methods=["GET"])
def item_to_show():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    data = dict(request.args)
    need = list()
    ordered_num = None
    if "max_num" in data:
        try:
            data["max_num"] = int(data["max_num"])
        except Exception as e:
            return make_response_json(400, "请求格式错误")
        else:
            ordered_num = 0
    if "range" in data:
        try:
            data["range"] = int(data["range"])
        except Exception as e:
            return make_response_json(400, "请求格式错误")
        else:
            td = timedelta(days=data["range"])
            last_time = date.today() - td
            need.append(Item.publish_time >= last_time)
    try:
        need_od = Item.select().where(*need).order_by(
            Item.publish_time.desc()).execute()
    except Exception as e:
        return make_response_json(500, f"查询发生错误 {repr(e)}")
    else:
        datas = {"show": list()}
        for i in need_od:
            j = i.__data__
            if current_user.state != User_state.Admin.value:
                j.pop("locaked_num")
            if ordered_num is not None:
                if ordered_num < data["max_num"]:
                    datas["show"].append(j)
                    ordered_num += 1
                else:
                    break
    return make_response_json(200, "返回订单", datas)
