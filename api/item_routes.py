#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import base64
from email.policy import default
from io import BytesIO
import shutil

import werkzeug
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state
from item import item_blue
from admin.models import Feedback, Feedback_kind, Feedback_state
from datetime import datetime, date, timedelta
from hashlib import md5
from difflib import SequenceMatcher
from PIL import Image


def createPath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)


@api_blue.route("/get_item_pics", methods=['GET'])
def get_item_pics():
    data = dict(request.args)
    try:
        item_id = int(data["item_id"])
    except Exception as e:
        return make_response_json(400, f"请求格式错误 {repr(e)}")
    try:
        item = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(400, "此物品不存在")
    pic_path = os.path.join(item_blue.static_folder,
                            f'resource/item_pic/{item_id}/pic')
    default_pic = os.path.join(item_blue.static_folder,
                               'resource/default_pic/test.jpg')
    if not os.path.exists(pic_path):
        createPath(pic_path)
    if len(os.listdir(pic_path)) == 0:
        shutil.copy(default_pic, pic_path)
    pic_list = os.listdir(pic_path)
    pics = list()
    for pic_name in pic_list:
        pics.append(
            url_for('item.static',
                    filename=f'resource/item_pic/{item_id}/pic/{pic_name}'))
    return make_response_json(200, "图片查找成功", data={"url": pics})


@api_blue.route("/get_item_head_pic", methods=['GET'])
def get_item_head_pic():
    data = dict(request.args)
    try:
        item_id = int(data["item_id"])
    except Exception as e:
        return make_response_json(400, f"请求格式错误 {repr(e)}")
    try:
        item = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(400, "此物品不存在")
    pic_path = os.path.join(item_blue.static_folder,
                            f'resource/item_pic/{item_id}/head')
    default_pic = os.path.join(item_blue.static_folder,
                               'resource/default_pic/test.jpg')
    if not os.path.exists(pic_path):
        createPath(pic_path)
    if len(os.listdir(pic_path)) == 0:
        shutil.copy(default_pic, pic_path)
    pic_list = os.listdir(pic_path)
    pic = url_for('item.static',
                  filename=f'resource/item_pic/{item_id}/head/{pic_list[0]}')
    return make_response_json(200, "图片查找成功", data={"url": pic})


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
    data = dict(request.args)
    try:
        user_id = int(data["user_id"])
    except:
        user_id = current_user.id
    else:
        try:
            user = User.get(User.id == user_id)
        except Exception as e:
            return make_response_json(404, "该用户不存在")
    try:
        item_list = Item.select().where(Item.user_id == user_id).execute()
    except Exception as e:
        return make_response_json(500, f"查询错误 {repr(e)}")
    datas = list()
    for i in item_list:
        j = i.__data__
        #j.pop('type')
        if current_user.state != User_state.Admin.value:
            j.pop('locked_num')
        j["publish_time"] = str(j["publish_time"])
        datas.append(j)
    return make_response_json(200, "查询成功", data=datas)


@api_blue.route('/search', methods=['POST'])
def get_search():
    data = request.get_json()
    try:
        search_type = int(data["search_type"])
    except Exception as e:
        return make_response_json(400, "请求格式错误")
    if search_type != Item_type.Goods.value and search_type != Item_type.Want.value:
        return make_response_json(400, "搜索类型仅能指定商品或悬赏")
    if "key_word" in data:
        key_word = data["key_word"]
    else:
        return make_response_json(400, "请输入关键词")
    if "order_type" in data:
        order_type = data["order_type"]
    else:
        order_type = "name"
    #get_data = Item.select().where().exectue()

    need = (Item.id, Item.name, Item.user_id, Item.publish_time, Item.price,
            Item.tag)
    select_need = [Item.name.contains(key_word), Item.type == search_type]
    try:
        if "start_time" in data:
            start_time = data["start_time"]
            if start_time != "" and start_time is not None:
                start_time = datetime.strptime(start_time, "%Y-%m-%d")
                select_need.append(Item.publish_time >= start_time)
        if "end_time" in data:
            end_time = data["end_time"]
            if end_time != "" and end_time is not None:
                end_time = datetime.strptime(end_time, "%Y-%m-%d")
                select_need.append(Item.publish_time <= end_time)
    except Exception as e:
        print(e)
        return make_response_json(400, '时间格式错误,应为年-月-日格式')
    else:
        get_data = Item.select(*need).where(*select_need).execute()
        datas = [i.__data__ for i in get_data]
        new_data = list()
        if order_type == "time":
            datas.sort(key=lambda x: x["publish_time"], reverse=True)
        elif order_type == "price":
            datas.sort(key=lambda x: x["price"], reverse=False)
        else:
            #orderWay = (Item.publish_time.desc(), )  # 改：默认其实为相似度
            datas.sort(
                key=lambda x: SequenceMatcher(a=key_word, b=x["name"]).ratio(),
                reverse=True)
        for i in datas:
            i['price'] = float(i['price'])
            i['publish_time'] = str(i['publish_time'])
            new_data.append(i)
        return make_response_json(200, "搜索结果如下", new_data)


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
        data["id"] = int(data["id"])
        if "shelved_num" in data:
            data["shelved_num"] = int(data["shelved_num"])
        if "locked_num" in data:
            data["locked_num"] = int(data["locked_num"])
        if "price" in data:
            data["price"] = float(data["price"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    try:
        item = Item.get(Item.id == data["id"])
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
            if current_user.id != item.user_id.id:
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
    try:
        price = float(data["price"])
        item_type = int(data["type"])
        shelved_num = int(data["shelved_num"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    if price <= 0:
        return make_response_json(400, "请求格式不对")
    if item_type != Item_type.Goods.value and item_type != Item_type.Want.value:
        return make_response_json(400, "仅能上传物品")
    if shelved_num <= 0:
        return make_response_json(400, "不允许发布负数个物品")
    data["user_id"] = current_user.id
    data["publish_time"] = datetime.now()
    try:
        new = Item.create(**data)
    except Exception as e:
        return make_response_json(500, f"上传失败\n{str(e)}:{repr(e)}")
    createPath(
        os.path.join(item_blue.static_folder,
                     f'resource/item_pic/{new.id}/head'))
    createPath(
        os.path.join(item_blue.static_folder,
                     f'resource/item_pic/{new.id}/pic'))
    default_pic = os.path.join(item_blue.static_folder,
                               'resource/default_pic/test.jpg')
    curpath = os.path.join(item_blue.static_folder,
                           f'resource/item_pic/{new.id}/')
    tempath = os.path.join(item_blue.static_folder, f'resource/temp/')
    if len(data["urls"]) == 0:
        #给一个默认图
        shutil.copy(default_pic, os.path.join(curpath, 'head/'))
        shutil.copy(default_pic, os.path.join(curpath, 'pic/'))

    else:
        head_pics = [i["MD5"] for i in data["urls"] if i["is_cover_pic"]]
        if len(head_pics) == 0:
            head_pic = data["urls"][0]["MD5"]
        elif len(head_pics) > 1:
            new.delete_instance()
            return make_response_json(400, "仅能选定一张头图")
        else:
            head_pic = head_pics[0]
        shutil.copy(os.path.join(tempath, head_pic),
                    os.path.join(curpath, 'head/'))
        for j in data["urls"]:
            shutil.move(os.path.join(tempath, j["MD5"]),
                        os.path.join(curpath, 'pic/'))
        #将所有的图片转到用户对应文件夹
    return make_response_json(200, "上传成功")


def get_pillow_img_form_data_stream(data):
    '''
    传入request.files.get('something') (data类型为werkzeug.filestorage)
    将图片读取后按WEBP转换，保存入临时图床文件夹
    最后返回{400，失败}或{200，成功，md5(str)}
    '''
    try:
        #os.path.join(item_blue.static_folder, f'resource/temp')
        #或
        #url_for('item.static', filename=f'resource/item_pic/{item_id}/[head|pic]')
        curpath = os.path.join(item_blue.static_folder, f'resource/temp')
        createPath(curpath)

        path_name = os.path.join(curpath, data.filename)
        createPath(curpath)
        data.save(path_name)
        img = Image.open(path_name)
        md5_str = md5(img.tobytes()).hexdigest()
        os.remove(path_name)

        path_name_new = os.path.join(curpath, f'{md5_str}')
        img.save(path_name_new, 'WEBP')
        img = Image.open(path_name_new)
        md5_str = md5(img.tobytes()).hexdigest()
        os.remove(path_name_new)

        path_name_new = os.path.join(curpath, f'{md5_str}')
        #if os.path.exists(path_name_new):
        #    return make_response_json(400, f"上传图片失败：请勿重复上传图片")
        img.save(path_name_new, 'WEBP')
    except Exception as e:
        print(e)
        return make_response_json(400, f"上传图片失败：文件格式错误或损坏")
    else:
        return make_response_json(200, "上传图片成功", md5_str)


@api_blue.route("/post_item_pic", methods=["POST"])
def post_item_pic():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    return get_pillow_img_form_data_stream(request.files.get('file'))


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
    print(request.get_json())
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
    tep = Favor.select().where(Favor.user_id == current_user.id)
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
    tep = History.select().where(History.user_id == current_user.id)
    data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        res['visit_time'] = str(i.visit_time)
        data.append(res)
    return make_response_json(200, "操作成功", data)


@api_blue.route("/delete_history", methods=["DELETE"])
def item_delete_history():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    print(request.get_json())
    req = request.get_json()["item_id_list"]

    #tep = Item.select().where(Item.id << req)  #在一个列表中查询
    #if tep.count() != len(req):  #长度对不上
    #    return make_response_json(404, "不存在对应物品")
    try:
        NotFound = False
        for i in req:
            tep = History.select().where((History.user_id == current_user.id)
                                         & (History.item_id == i))

            if tep.count() <= 0:
                NotFound = True
            else:
                History.delete().where((History.user_id == current_user.id)
                                       & (History.item_id == i)).execute()
        if NotFound == True:
            return make_response_json(404, "不存在对应的历史")
        return make_response_json(200, "删除成功")
    except Exception as e:
        return make_response_json(500, f"发生错误 {repr(e)}")


@api_blue.route("/report", methods=["POST"])
def report():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户还未登陆")
    data = request.get_json()
    feed_data = dict()
    feed_data["user_id"] = current_user.id
    feed_data["publish_time"] = date.today()
    feed_data["state"] = Feedback_state.Unread.value
    try:
        kind = int(data['kind'])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    feed_data["kind"] = kind
    if 'reason' in data:
        reason = data["reason"]
    else:
        reason = ""
    if kind == Feedback_kind.Item.value:
        try:
            item_id = int(data['item_id'])
        except Exception as e:
            return make_response_json(400, "请求格式不对")
        try:
            item = Item.get(Item.id == item_id)
        except Exception as e:
            return make_response_json(404, "待举报的物品不存在")
        reason += "物品id:{} 物品名称:{} ".format(item.id, item.name)
    elif kind == Feedback_kind.User.value:
        try:
            user_id = int(data["user_id"])
        except Exception as e:
            return make_response_json(400, "请求格式不对")
        try:
            user = User.get(User.id == user_id)
        except Exception as e:
            return make_response_json(404, "待举报的用户不存在")
        reason += "用户id:{} 用户名称:{} ".format(user.id, user.name)
    else:
        pass
    feed_data["feedback_content"] = reason
    try:
        Feedback.create(**feed_data)
    except Exception as e:
        return make_response_json(500, f"存储时发生错误 {repr(e)}")
    return make_response_json(200, "举报完成,请等待管理员处理...")


@api_blue.route("/item_to_show", methods=["GET"])
def item_to_show():
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
        if len(need):
            need_od = Item.select().where(*need).order_by(
                Item.publish_time.desc()).execute()
        else:
            need_od = Item.select().order_by(
                Item.publish_time.desc()).execute()
    except Exception as e:
        return make_response_json(500, f"查询发生错误 {repr(e)}")
    else:
        datas = {"show": list()}
        for i in need_od:
            j = i.__data__
            j.pop("locked_num")
            j["publish_time"] = str(j["publish_time"])
            if ordered_num is not None:
                if ordered_num < data["max_num"]:
                    datas["show"].append(j)
                    ordered_num += 1
                else:
                    break
            else:
                datas["show"].append(j)
    return make_response_json(200, "返回订单", datas)
