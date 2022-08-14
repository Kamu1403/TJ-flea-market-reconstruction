#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import base64
from io import BytesIO
import shutil

import werkzeug
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state, Item_tag_type
from item import item_blue
from admin.models import Feedback, Feedback_kind, Feedback_state
from datetime import datetime, date, timedelta
from hashlib import md5
from difflib import SequenceMatcher
from PIL import Image
from numpy import float32 as Float


def createPath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)


# 接口/get_item_pics与/get_item_head_pic的公共函数
def get_pic(data, select_pics):
    try:
        item_id = int(data["item_id"])
    except Exception as e:
        return make_response_json(400, f"请求格式错误 {repr(e)}")
    try:
        item = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(400, "此物品不存在")
    pic_path = ''
    if select_pics:
        pic_path = os.path.join(item_blue.static_folder,
                                f'resource/item_pic/{item_id}/pic')
    else:
        pic_path = os.path.join(item_blue.static_folder,
                                f'resource/item_pic/{item_id}/head')
    default_pic = os.path.join(item_blue.static_folder,
                               'resource/default_pic/test.jpg')
    if not os.path.exists(pic_path):
        createPath(pic_path)
    if len(os.listdir(pic_path)) == 0:
        shutil.copy(default_pic, pic_path)
    pic_list = os.listdir(pic_path)

    if select_pics:
        pics = list()
        for pic_name in pic_list:
            pics.append(
                url_for(
                    'item.static',
                    filename=f'resource/item_pic/{item_id}/pic/{pic_name}'))
        return make_response_json(200, "图片查找成功", data={"url": pics})
    else:
        pic = url_for(
            'item.static',
            filename=f'resource/item_pic/{item_id}/head/{pic_list[0]}')
        return make_response_json(200, "图片查找成功", data={"url": pic})


@api_blue.route("/get_item_pics", methods=['GET'])
def get_item_pics():
    data = dict(request.args)
    return get_pic(data, True)
    '''
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
    '''


@api_blue.route("/get_item_head_pic", methods=['GET'])
def get_item_head_pic():
    data = dict(request.args)
    return get_pic(data, False)
    '''
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
    '''


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
        res["data"] = dic
        dic.pop('id')
        dic.pop('locked_num')
        dic['publish_time'] = str(dic['publish_time'])
        dic['price'] = float(dic['price'])
        if not current_user.is_authenticated:
            is_admin = False
            is_pub = False
        else:
            is_admin = (current_user.state == User_state.Admin.value)
            is_pub = (it.user_id.id == current_user.id)
        res["is_admin"] = is_admin
        res["is_pub"] = is_pub
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


#接口search的拆分函数
def data_check(data): #请求数据检查
    if "range_min" in data or "range_max" in data:
        if "range_min" in data and "range_max" in data:
            range_min = int(data["range_min"])
            range_max = int(data["range_max"])
        else:
            raise Exception('请求格式错误')
    else:
        range_min = 0
        range_max = 50
    
    search_type = int(data["search_type"])

    if "key_word" in data:
        key_word = data["key_word"]
    else:
        raise Exception('请输入关键词')

    if "order_type" in data:
        order_type = data["order_type"]
    else:
        order_type = "name"

    return range_min, range_max, search_type, key_word, order_type

def select_need_append(key_word, search_type, data): #搜索依据添加
    select_need = [Item.name.contains(key_word)]
    if search_type in Item_type._value2member_map_:
        select_need.append(Item.type == search_type)
    if "tag" in data:
        if data["tag"] not in Item_tag_type._value2member_map_:
            raise Exception('请求格式错误')
        else:
            select_need.append(Item.tag == data["tag"])

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
    
    return select_need

def search(need, select_need, order_type, key_word, range_min, range_max): #实现搜索结果
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
    range_max = min(len(new_data), range_max)
    final_data = {
        "total_count": len(new_data),
        "item_list": new_data[range_min:range_max]
    }
    return make_response_json(200, "搜索结果如下", data=final_data)

@api_blue.route('/search', methods=['POST'])
def get_search():
    data = request.get_json()
    try:
        range_min, range_max, search_type, key_word, order_type = data_check(data)
        need = (Item.id, Item.name, Item.user_id, Item.publish_time, Item.price,
            Item.tag)
        select_need = select_need_append(key_word, search_type, data)
    except:
        return make_response_json(400, "请求格式错误")
    else:
        return search(need, select_need, order_type, key_word, range_min, range_max)

'''
@api_blue.route('/search', methods=['POST'])
def get_search():
    data = request.get_json()
    if "range_min" in data or "range_max" in data:
        if "range_min" in data and "range_max" in data:
            try:
                range_min = int(data["range_min"])
                range_max = int(data["range_max"])
            except Exception as e:
                return make_response_json(400, "请求格式错误")
        else:
            return make_response_json(400, "请求格式错误")
    else:
        range_min = 0
        range_max = 50
    try:
        search_type = int(data["search_type"])
    except Exception as e:
        return make_response_json(400, "请求格式错误")
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
    select_need = [Item.name.contains(key_word)]
    if search_type in Item_type._value2member_map_:
        select_need.append(Item.type == search_type)
    if "tag" in data:
        if data["tag"] not in Item_tag_type._value2member_map_:
            return make_response_json(400, "请求格式错误")
        else:
            select_need.append(Item.tag == data["tag"])
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
        range_max = min(len(new_data), range_max)
        final_data = {
            "total_count": len(new_data),
            "item_list": new_data[range_min:range_max]
        }
        return make_response_json(200, "搜索结果如下", data=final_data)
'''


@api_blue.route("/change_item_state", methods=["PUT"])
def change_item_state():
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
        if item.state == data["state"]:
            return make_response_json(400, "商品当前状态和希望更改的状态相同")
        else:
            if current_user.state == User_state.Admin.value:
                item.state = data["state"]
                # if data["state"] == User_state.Freeze.value:
                #     向物品所有者发布一条消息
                #       pass
                if data["state"] == Item_state.Freeze.value:
                    if item.type == Item_type.Goods.value:
                        send_message(SYS_ADMIN_NO, item.user_id.id,
                                     f"您的商品<{item.name}>被系统管理员下架")
                    elif item.type == Item_type.Want.value:
                        send_message(SYS_ADMIN_NO, item.user_id.id,
                                     f"您的悬赏<{item.name}>被系统管理员下架")
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
    if data["num"] < 0:
        return make_response_json(400, "不允许负数物品存在")
    if data["num"].bit_length() > Item.shelved_num.__sizeof__() - 1:
        return make_response_json(400, "数量越界")
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
    if "tag" not in data:
        return make_response_json(400, "请选择物品类型")
    if data["tag"] not in Item_tag_type._value2member_map_:
        return make_response_json(400, "请求格式错误")
    if len(data["name"]) > 40:
        return make_response_json(400, "名称过长")
    if len(data["description"]) > Item.description.max_length:
        return make_response_json(400, "描述过长")
    try:
        data["id"] = int(data["id"])
        if "shelved_num" in data:
            data["shelved_num"] = int(data["shelved_num"])
        if "price" in data:
            data["price"] = Float(data["price"])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    if data["shelved_num"] < 0:
        return make_response_json(400, "不允许负数商品个数")
    if data["price"] == Float("inf") or data["price"] == Float("nan"):
        return make_response_json(400, "价格越界")
    if data["price"] <= 0:
        return make_response_json(400, "不允许非正数价格")
    if data["shelved_num"].bit_length() > Item.shelved_num.__sizeof__() - 1:
        return make_response_json(400, "数量越界")
    try:
        item = Item.get(Item.id == data["id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if current_user.state == User_state.Admin.value:
            for i in data:
                if i in item.__data__:
                    exec(f"item.{i} = data['{i}']")
            item.save()
            return make_response_json(200, "操作成功")
        elif current_user.state == User_state.Under_ban.value:
            return make_response_json(401, "您当前已被封号,请联系管理员解封")
        else:
            if current_user.id != item.user_id.id:
                return make_response_json(401, "不可改变其他人的商品状态")
            else:
                for i in data:
                    if i in item.__data__:
                        exec(f"item.{i} = data['{i}']")
                item.save()
                return make_response_json(200, "操作成功")


def trans_square(image):
    r"""Open the image using PIL."""
    image = image.convert('RGB')
    w, h = image.size
    background = Image.new('RGB',
                           size=(max(w, h), max(w, h)),
                           color=(255, 255, 255))  # 创建背景图，颜色值为127
    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
    background.paste(image, box)
    return background


@api_blue.route("/post_item_info", methods=["POST"])
def post_item_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    if current_user.state == User_state.Under_ban.value:
        return make_response_json(401, "当前用户已被封号")
    data = request.get_json()
    if len(data["name"]) > 40:
        return make_response_json(400, "名称过长")
    if len(data["description"]) > Item.description.max_length:
        return make_response_json(
            400, f"描述过长,应限制在{Item.description.max_length}字以内")
    if "tag" not in data:
        return make_response_json(400, "请选择物品类型")
    if data["tag"] not in Item_tag_type._value2member_map_:
        return make_response_json(400, "请求格式错误")
    try:

        price = Float(data["price"])
        item_type = int(data["type"])
        shelved_num = int(data["shelved_num"])
    except Exception as e:
        return make_response_json(400, "数据类型错误")
    if price == Float("inf") or price == Float("nan"):
        return make_response_json(400, "价格越界")
    if price <= 1e-8:
        return make_response_json(400, "价格越界")
    if item_type != Item_type.Goods.value and item_type != Item_type.Want.value:
        return make_response_json(400, "仅能上传物品")
    if shelved_num <= 0:
        return make_response_json(400, "数量越界")
    if shelved_num.bit_length() > Item.shelved_num.__sizeof__() - 1:
        return make_response_json(400, "数量越界")
    data["user_id"] = current_user.id
    data["publish_time"] = datetime.now()
    try:
        new = Item.create(**data)
    except Exception as e:
        return make_response_json(500, f"上传失败：{repr(e)}")
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
            #new.delete_instance()
            #return make_response_json(400, "仅能选定一张头图")
            head_pic = head_pics[0]
        else:
            head_pic = head_pics[0]
        shutil.copy(os.path.join(tempath, head_pic),
                    os.path.join(curpath, 'head/'))

        img = Image.open(os.path.join(curpath, 'head/', head_pic))
        img = trans_square(img)
        #img.show()
        img.save(os.path.join(curpath, 'head/', head_pic), 'WEBP')

        for j in data["urls"]:
            shutil.move(os.path.join(tempath, j["MD5"]),
                        os.path.join(curpath, 'pic/'))
        #将所有的图片转到用户对应文件夹
    return make_response_json(200, "上传成功",
                              {"url": url_for('item.content', item_id=new.id)})


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
        w, h = img.size
        ratio = max(w, h) / 1920
        if ratio > 1:
            img = img.resize((int(w / ratio), int(h / ratio)))
        ratio = 250 / min(w, h)
        if ratio > 1:
            img = img.resize((int(w * ratio), int(h * ratio)))
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
def delete_favor():
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
def get_favor():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    req = dict(request.args)
    if "range_min" in req or "range_max" in req:
        if "range_min" in req and "range_max" in req:
            try:
                range_min = int(req["range_min"])
                range_max = int(req["rang_max"])
            except Exception as e:
                return make_response_json(400, "请求格式错误")
        else:
            return make_response_json("请求格式错误")
    else:
        range_min = 0
        range_max = 50
    tep = Favor.select().where(Favor.user_id == current_user.id).order_by(
        Favor.collect_time.desc())
    fav_data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        res['collect_time'] = str(i.collect_time)
        fav_data.append(res)
    range_max = min(len(fav_data), range_max)
    data = {
        "total_count": len(fav_data),
        "favor_list": fav_data[range_min:range_max]
    }
    return make_response_json(200, "操作成功", data)


@api_blue.route("/get_item_favor", methods=["GET"])
def get_item_favor():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    try:
        item_id = int(request.args["item_id"])
    except:
        return make_response_json(400, "格式错误")
    try:
        tep = Favor.get(Favor.user_id == current_user.id,
                        Favor.item_id == item_id)
    except:
        return make_response_json(200, "操作成功", False)
    else:
        return make_response_json(200, "操作成功", True)


@api_blue.route("/get_history", methods=["GET"])
def get_history():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    req = dict(request.args)
    if "range_min" in req or "range_max" in req:
        if "range_min" in req and "range_max" in req:
            try:
                range_min = int(req["range_min"])
                range_max = int(req["rang_max"])
            except Exception as e:
                return make_response_json(400, "请求格式错误")
        else:
            return make_response_json("请求格式错误")
    else:
        range_min = 0
        range_max = 50
    tep = History.select().where(History.user_id == current_user.id).order_by(
        History.visit_time.desc())
    his_data = []
    for i in tep:
        res = dict()
        res['id'] = i.id
        res['item_id'] = i.item_id.id
        res['visit_time'] = str(i.visit_time)
        his_data.append(res)
    range_max = min(len(his_data), range_max)
    data = {
        "total_count": len(his_data),
        "history_list": his_data[range_min:range_max]
    }
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
    feedback_data = dict()
    feedback_data["user_id"] = current_user.id
    feedback_data["publish_time"] = datetime.now()
    feedback_data["state"] = Feedback_state.Unread.value
    try:
        kind = int(data['kind'])
    except Exception as e:
        return make_response_json(400, "请求格式不对")
    if kind not in [
            eval(f"Feedback_kind.{i}.value") for i in Feedback_kind.__members__
    ]:
        return make_response_json(400, "请求格式不对")
    feedback_data["kind"] = kind
    if 'reason' in data:
        reason = data["reason"]
    else:
        reason = ""
    if len(reason) > Feedback.feedback_content.max_length // 2:
        return make_response_json(
            400, f"反馈过长,应限制在{Feedback.feedback_content.max_length//2}字以内")
    if kind == Feedback_kind.Item.value:
        try:
            item_id = int(data['item_id'])
        except Exception as e:
            return make_response_json(400, "请求格式不对")
        try:
            item = Item.get(Item.id == item_id)
        except Exception as e:
            return make_response_json(404, "您举报的物品不存在")
        if item.user_id.id == current_user.id:
            return make_response_json(400, "不可举报自己的物品")
        reason = "物品id:{} ".format(item.id) + reason
    elif kind == Feedback_kind.User.value:
        try:
            user_id = int(data["user_id"])
        except Exception as e:
            return make_response_json(400, "请求格式不对")
        try:
            user = User.get(User.id == user_id)
        except Exception as e:
            return make_response_json(404, "您举报的用户不存在")
        if user.id == current_user.id:
            return make_response_json(400, "不可举报自己")
        reason = "用户id:{} ".format(user.id) + reason
    else:
        pass
    feedback_data["feedback_content"] = reason
    try:
        Feedback.create(**feedback_data)
    except Exception as e:
        return make_response_json(500, f"存储时发生错误 {repr(e)}")
    return make_response_json(200, "举报完成,请等待管理员处理...")


@api_blue.route("/item_to_show", methods=["GET"])
def item_to_show():
    data = dict(request.args)
    need = list()
    ordered_num = None
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
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
            last_time = datetime.now() - td
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
            if j["state"] == Item_state.Sale.value:
                if ordered_num is not None:
                    if ordered_num < data["max_num"]:
                        if user_id is None or user_id != j["user_id"]:
                            datas["show"].append(j)
                            ordered_num += 1
                    else:
                        break
                else:
                    if user_id is None or user_id != j["user_id"]:
                        datas["show"].append(j)
    return make_response_json(200, "返回订单", datas)


@api_blue.route("/get_class", methods=["GET"])
def get_class():
    return make_response_json(
        200,
        "类别如下",
        data={"class": list(Item_tag_type._value2member_map_.keys())})
