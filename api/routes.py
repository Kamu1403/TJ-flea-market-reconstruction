#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from operator import methodcaller
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
import os
import re
import json
import datetime
import time

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


def judge_user_id(user_id: str):
    try:
        user_id = str(user_id).strip()
    except:
        return [400, "账号格式错误"]
    if '@' not in user_id:
        user_id += "@tongji.edu.cn"
    pattern = re.compile(r'^\d{7}@tongji\.edu\.cn$')
    result = pattern.findall(user_id)
    if len(result) > 0:
        return [0, "验证通过"]
    pattern = re.compile(r'@tongji\.edu\.cn$')
    result = pattern.findall(user_id)
    if len(result) > 1:
        return [400, "邮箱账号必须为学号！"]
    return [400, "账号格式错误"]


curpath = os.path.dirname(__file__)
config = os.path.join(curpath, 'verify_code.json')  # [{"time": int(time.time()), "user_id":str, "code":str}]
if not os.path.exists(config):
    with open(config, "w", encoding="utf-8") as fp:
        print("[]", file=fp)


def save_verify_code(code: json):
    with open(config, "w", encoding="utf-8") as fp:
        json.dump(code, fp, indent=4, ensure_ascii=False)


def get_verify_code():
    with open(config, "r", encoding="utf-8") as fp:
        return (json.load(fp))


def judge_code(user_id: str, code: str) -> list:
    '''
    验证code：
    if 该用户下不存在验证码：400，验证码不存在，请点击发送验证码
    elif 验证码过期：400，验证码已过期，请重新点击发送验证码
    elif 验证码错误：400，验证码错误，请重新点击发送验证码
    '''
    try:
        code = str(code).strip()
    except:
        return [400, "验证码格式错误"]
    if len(code) == 0:
        return [400, "验证码不可为空"]

    jui = judge_user_id(user_id)
    if jui[0] != 0:
        return jui
    code_list = get_verify_code()
    save_verify_code(list(filter(lambda x: x["time"] - time < 900, code_list)))  # 验证码有效期15min
    nowtime = int(time.time())
    code_exist_but_wrong = False
    code_exist_but_outofdate = False
    for i, code_record in enumerate(code_list):
        if code_record["user_id"] == user_id:
            if nowtime - code_record["time"] <= 900:
                if code_record["code"] == code:
                    return [0, "验证成功"]
                code_exist_but_wrong = True
            else:
                code_exist_but_outofdate = True

    if code_exist_but_wrong:
        return [400, "验证码错误"]
    if code_exist_but_outofdate:
        return [400, "验证码过期，请重新获取验证码"]
    return [400, "验证码不存在，请先获取验证码"]


def judge_password(password: str):
    if type(password) != str:
        return [400, "密码格式错误"]
    if len(password) < 6:
        return [400, "密码过短"]
    if len(password) > 32:
        return [400, "密码过长"]
    pattern = re.compile(r'[a-zA-Z0-9_-]')
    result = pattern.findall(password)
    if len(result) != len(password):
        return [400, "密码含有非法字符"]
    return [0, "验证通过"]


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
