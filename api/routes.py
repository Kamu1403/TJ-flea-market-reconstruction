#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from operator import methodcaller
from tkinter import W
from flask_login import current_user
from api import api_blue
from flask import make_response, request, jsonify
#enum
from user.models import User_state
from admin.models import Feedback_kind, Feedback_state
from order.models import Order_state
#model
from user.models import User
from admin.models import Feedback, User_Management
from order.models import Contact, Review, Order, Order_State_Item, Order_Item
from item.models import Goods, Want, HistoryGoods, HistoryWant, FavorGoods, FavorWant
import copy

#返回值规范
default_res = {'success': True, 'statusCode': 200, 'message': '', 'data': {}}
'''
statusCode:
•	200：操作成功返回。
•	201：表示创建成功，POST 添加数据成功后必须返回此状态码。
•	400：请求格式不对。
•	401：未授权。（User/Admin）
•	404：请求的资源未找到。
•	500：内部程序错误。

其他详见接口文档
'''
"""
@api_blue.route('',method=['POST'])
def login_using_password():
    res=copy.deepcopy(default_res)
    if request.method == 'POST':
        user_id=request.form.get('user_id')
        password=request.form.get('password')
        remember_me=True
        try:
            user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否时管理员
        except:
            flash('无效的学号,请检查输入或注册')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        else:
            # 查到了，判断密码
            if not user.check_password(password):
                # 如果用户不存在或者密码不正确就会闪现这条信息
                flash('密码错误')
                # 然后重定向到登录页面
                return redirect(url_for('login'))
            if user.state==-1:
                #被封号了
                flash("您已被封号")
                # 然后重定向到登录页面
                return redirect(url_for('login'))

            # 记住登录状态，同时维护current_user
            login_user(user, remember=remember_me)
            return redirect(url_for('user.index'))

"""


def GetUserDict(i) -> dict:
    user = {}
    user['id'] = i.id
    user['username'] = i.username
    user['email'] = i.email
    user['state'] = i.state
    user['score'] = i.score
    user['telephone'] = i.telephone
    user['wechat'] = i.wechat
    user['qq_number'] = i.qq_number
    user['campus_branch'] = i.campus_branch
    user['dormitory'] = i.dormitory
    user['gender'] = i.gender
    user['name_is_published'] = i.name_is_published
    if i.name_is_published == True:
        user['name'] = i.name
    else:
        user['name'] = '保密'
    user['major_is_published'] = i.major_is_published
    if i.major_is_published == True:
        user['major'] = i.major
    else:
        user['major'] = '保密'
    return user


#管理员获取所有用户信息
@api_blue.route('/getalluser', methods=['GET'])
def get_all_user():
    res = copy.deepcopy(default_res)
    data_list = []
    # 判断当前用户是否验证
    if not current_user.is_authenticated:
        res['message'] = "该用户未通过验证"
        res['statusCode'] = 401
        res['success'] = False
    elif current_user.state == User_state.Admin.value:  #如果当前用户是管理员
        users = User.select().where(User.state != User_state.Admin.value)
        for i in users:
            user_dic = GetUserDict(i)
            data_list.append(user_dic)
        res['data'] = data_list

        if len(data_list) > 0:
            res['message'] = "所有用户信息获取成功"
        else:
            res['message'] = "未找到对应用户信息"
            res['statusCode'] = 404
            res['success'] = False

    else:  #非管理员
        res['message'] = "非管理员无此权限"
        res['statusCode'] = 401
        res['success'] = False

    return make_response(jsonify(res))


#管理员封号
@api_blue.route('/banuser', methods=['PUT'])
def ban_user():
    if request.method == 'PUT':
        res = copy.deepcopy(default_res)
        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        #在APIFOX测试运行时current_user未经认证，需要先在apifox上登录后才current_user才有效
        elif current_user.state == User_state.Admin.value:  #如果当前用户是管理员
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['message'] = "已将对应用户封号"
                tep.state = -1
                tep.save()
                #query=User.update(state=-1).where(User.id==user_id)
                #query.execute()
        else:  #非管理员
            res['message'] = "非管理员无此权限"
            res['statusCode'] = 401
            res['success'] = False

        return make_response(jsonify(res))


@api_blue.route('/getuserinfo', methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        res = copy.deepcopy(default_res)

        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        else:
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['data'] = GetUserDict(tep)
                res['message'] = "获取用户数据成功"
        return make_response(jsonify(res))

"""
@api_blue.route('/getlatestorder', methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        res = copy.deepcopy(default_res)

        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        else:
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['data'] = GetUserDict(tep)
                res['message'] = "获取用户数据成功"
        return make_response(jsonify(res))
"""
@api_blue.route('/get_item_info',methods=['GET'])
def get_item_info():
    item_id = request.args.get('id')
    need_type = request.args.get("type")
    if need_type == "goods":
        bases = Goods
    elif need_type == "want":
        bases = Want
    else:
        bases = None
    res = copy.deepcopy(default_res)
    try:
        it = bases.get(bases.id==item_id)
    except Exception as e:
        it = None
    if it is None:
        #报错
        res['statusCode'] = 404
        res['success'] = False
        res['message'] = "未找到商品信息"
        res['data'] = dict()
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
            isPub = (it.publisher_id.id == current_user.id)
        res["isAdmin"] = isAdmin
        res["isPub"] = isPub
    return make_response(jsonify(res))

@api_blue.route('/search',methods=['POST'])
def get_search():
    search_type = request.form.get("search_type")
    key_word = request.form.get("key_word")
    order_type = request.form.get("order_type")
    res = copy.deepcopy(default_res)
    res['data'] = list()
    if search_type == "goods":
        bases = Goods
    elif search_type == "want":
        bases = Want
    else:
        bases = None
    if bases is None:
        res['statusCode'] = 400
        res['message'] = "搜索类型仅能指定商品或悬赏"
        res['success'] = False
    else:
        #get_data = bases.select().where().exectue()
        if order_type == "time":
            orderWay = bases.publish_time.asc()
        elif order_type == "price":
            orderWay == bases.publish_time.asc()
        elif order_type == "name":
            orderWay = bases.publish_time.asc()
        else:
            orderWay = None
        if orderWay is not None:
            res['statusCode'] = 200
            res['message'] = "已搜索如下结果"
            res['success'] = True
            need = (bases.name,bases.publisher_id,bases.publish_time,bases.price)
            select_need = (bases.name.contains(key_word),)
            get_data = bases.select(*need).where(*select_need).order_by(orderWay).execute()
            for i in get_data:
                j = i.__data__
                j['price'] = float(j['price'])
                j['type'] = search_type
                res['data'].append(j)
            #order
        else:
            res['statusCode'] = 400
            res['message'] = "排序类型仅能指定价格、时间或内容相似度"
            res['success'] = False
    return make_response(jsonify(res))
