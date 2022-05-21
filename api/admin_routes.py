#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue


def GetUserDict(i) -> dict:
    user = {}
    user['id'] = i.id
    user['username'] = i.username
    user['email'] = i.email
    user['state'] = i.state
    user['score'] = i.score
    user['gender'] = i.gender
    user['user_no_is_published'] = i.user_no_is_published
    if i.user_no_is_published == True:
        user['user_no'] = i.user_no
    user['telephone_is_published'] = i.telephone_is_published
    if i.telephone_is_published == True:
        user['telephone'] = i.telephone
    user['wechat_is_published'] = i.wechat_is_published
    if i.wechat_is_published == True:
        user['wechat'] = i.wechat
    user['qq_is_published'] = i.qq_is_published
    if i.qq_is_published == True:
        user['qq_number'] = i.qq_number
    user['campus_is_published'] = i.campus_is_published
    if i.campus_is_published == True:
        user['campus_branch'] = i.campus_branch

    user['dormitory_is_published'] = i.dormitory_is_published
    if i.dormitory_is_published == True:
        user['dormitory'] = i.dormitory

    user['name_is_published'] = i.name_is_published
    if i.name_is_published == True:
        user['name'] = i.name

    user['major_is_published'] = i.major_is_published
    if i.major_is_published == True:
        user['major'] = i.major

    return user


#管理员获取所有用户信息
@api_blue.route('/get_all_user', methods=['GET'])
def get_all_user():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    if current_user.state < User_state.Admin.value:
        return make_response_json(401, "权限不足")

    users = User.select().where(User.state != User_state.Admin.value)
    data_list = []
    for i in users:
        user_dic = GetUserDict(i)
        data_list.append(user_dic)

    if len(data_list) == 0:
        return make_response_json(404, "无用户信息")
    return make_response_json(200, "所有用户信息获取成功", data_list)


#管理员封号
@api_blue.route('/ban_user', methods=['PUT'])
def ban_user():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    if current_user.state < User_state.Admin.value:
        return make_response_json(401, "权限不足")

    #在APIFOX测试运行时current_user未经认证，需要先在apifox上登录后才current_user才有效
    user_id = request.form.get("user_id")
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        tep.state = User_state.Under_ban.value
        tep.save()
        return make_response_json(200, "操作成功")

        #query=User.update(state=-1).where(User.id==user_id)
        #query.execute()


#访问其它用户
@api_blue.route('/get_user_info', methods=['POST'])
def get_user_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    user_id = request.form.get("user_id")
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        return make_response_json(200, "获取用户数据成功", GetUserDict(tep))
