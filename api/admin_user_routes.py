#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from datetime import datetime


def GetUserDict(i, is_self=False) -> dict:
    user = {}
    user['id'] = i.id
    user['username'] = i.username
    user['email'] = i.email
    user['state'] = i.state
    user['score'] = i.score
    user['gender'] = i.gender
    user['user_no_is_published'] = i.user_no_is_published
    if i.user_no_is_published == True or is_self:
        user['user_no'] = i.user_no
    user['telephone_is_published'] = i.telephone_is_published
    if i.telephone_is_published == True or is_self:
        user['telephone'] = i.telephone
    user['wechat_is_published'] = i.wechat_is_published
    if i.wechat_is_published == True or is_self:
        user['wechat'] = i.wechat
    user['qq_is_published'] = i.qq_is_published
    if i.qq_is_published == True or is_self:
        user['qq_number'] = i.qq_number
    user['campus_is_published'] = i.campus_is_published
    if i.campus_is_published == True or is_self:
        user['campus_branch'] = i.campus_branch

    user['dormitory_is_published'] = i.dormitory_is_published
    if i.dormitory_is_published == True or is_self:
        user['dormitory'] = i.dormitory

    user['name_is_published'] = i.name_is_published
    if i.name_is_published == True or is_self:
        user['name'] = i.name

    user['major_is_published'] = i.major_is_published
    if i.major_is_published == True or is_self:
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
        user_dic = GetUserDict(i, True)
        data_list.append(user_dic)

    if len(data_list) == 0:
        return make_response_json(404, "无用户信息")
    return make_response_json(200, "所有用户信息获取成功", data_list)


#管理员封号
@api_blue.route('/change_user_state', methods=['PUT'])
def change_user_state():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    if current_user.state < User_state.Admin.value:
        return make_response_json(401, "权限不足")

    #在APIFOX测试运行时current_user未经认证，需要先在apifox上登录后才current_user才有效
    req = request.get_json()
    try:
        user_id = int(req['user_id'])
        user_state = int(req['user_state'])
    except:
        return make_response_json(400, "请求格式不对")

    if user_state not in User_state._value2member_map_:
        return make_response_json(400, "请求格式不对")

    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        if tep.state == User_state.Admin.value:
            return make_response_json(400, "不可修改管理员状态")
        if user_state == User_state.Under_ban.value:
            try:
                ban_time = datetime.strptime(req["ban_time"], "%Y-%m-%d")
            except Exception as e:
                return make_response_json(400, "请求格式错误")
            if "ban_reason" not in req:
                return make_response_json(400, "请求格式错误")
            try:
                ban = User_Management.get(User_Management.user_id == user_id)
            except Exception as e:
                ban = User_Management.create(user_id=user_id,
                                             ban_time=ban_time,
                                             ban_reason=req["ban_reason"])
            else:
                ban.ban_time = ban_time
                ban.ban_reason = req["ban_reason"]
                ban.save()
            finally:
                tep.state = user_state
                tep.save()
                return make_response_json(200, "操作成功")
        elif user_state == User_state.Normal.value:
            if tep.state == User_state.Under_ban.value:
                try:
                    ban = User_Management.get(
                        User_Management.user_id == user_id)
                except Exception as e:
                    return make_response_json(500, "系统错误")
                ban.delete_instance()
                tep.state = user_state
                tep.save()
            return make_response_json(200, "操作成功")

        #query=User.update(state=-1).where(User.id==user_id)
        #query.execute()


#访问其它用户
@api_blue.route('/get_user_info', methods=['GET'])
def get_user_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")
    data = dict(request.args)
    if "user_id" in data:
        try:
            user_id = int(data['user_id'])
        except:
            return make_response_json(400, "请求格式错误")
    else:
        user_id = current_user.id
    #user_id = int(request.get_json()["user_id"])
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        return make_response_json(200, "获取用户数据成功",
                                  GetUserDict(tep, current_user.id == user_id))


#访问其它用户
@api_blue.route('/get_user_username', methods=['GET'])
def get_user_username():
    data = dict(request.args)
    try:
        user_id = int(data['user_id'])
    except:
        return make_response_json(400, "请求格式错误")
    #user_id = int(request.get_json()["user_id"])
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        return make_response_json(200, "获取用户数据姓名", {"name": tep.username})


@api_blue.route('/get_user_id', methods=["GET"])
def get_user_id():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")
    return make_response_json(200, "操作成功", {"user_id": current_user.id})


@api_blue.route('/change_user_info', methods=["PUT"])
def change_user_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")
    req = request.get_json()
    #print(req)
    try:
        tep = User.get(User.id == current_user.id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        try:
            if 'username' in req:
                tep.username = req['username']
            if 'gender' in req:
                tep.gender = req['gender']
            if 'user_no_is_published' in req:
                tep.user_no_is_published = req['user_no_is_published']
            if 'telephone_is_published' in req:
                tep.telephone_is_published = req['telephone_is_published']
            if 'telephone' in req:
                tep.telephone = req['telephone']
            if 'wechat_is_published' in req:
                tep.wechat_is_published = req['wechat_is_published']
            if 'wechat' in req:
                tep.wechat = req['wechat']
            if 'qq_is_published' in req:
                tep.qq_is_published = req['qq_is_published']
            if 'qq_number' in req:
                tep.qq_number = req['qq_number']
            if 'campus_is_published' in req:
                tep.campus_is_published = req['campus_is_published']
            if 'campus_branch' in req:
                tep.campus_branch = req['campus_branch']
            if 'dormitory_is_published' in req:
                tep.dormitory_is_published = req['dormitory_is_published']
            if 'dormitory' in req:
                tep.dormitory = req['dormitory']
            if 'name_is_published' in req:
                tep.name_is_published = req['name_is_published']
            if 'name' in req:
                tep.name = req['name']
            if 'major_is_published' in req:
                tep.major_is_published = req['major_is_published']
            if 'major' in req:
                tep.major = req['major']
            tep.save()  #保存
        except Exception as e:
            return make_response_json(500, "程序发生如下错误:\n{}".format(e))
        else:
            return make_response_json(200, "操作成功")


@api_blue.route("/get_reports", methods=["GET"])
def get_reports():
    if not current_user.is_authenticated or current_user.state != User_state.Admin.value:
        return make_response_json(401, "用户无权访问")
    try:
        datas = Feedback.select(Feedback.id, Feedback.state).order_by(
            Feedback.publish_time).execute()
    except Exception as e:
        return make_response_json(500, f"系统发生故障 {repr(e)}")
    data = {str(i): list() for i in Feedback_state._value2member_map_}
    for i in datas:
        data[str(i.state)].append(i.id)
    return make_response_json(200, "查询结果如下", data=data)


@api_blue.route("/admin_get_report", methods=["GET"])
def admin_get_report():
    if not current_user.is_authenticated or current_user.state != User_state.Admin.value:
        return make_response_json(401, "用户无权访问")
    data = dict(request.args)
    try:
        feedback_id = int(data["feedback_id"])
    except Exception as e:
        return make_response_json(400, "请求格式错误")
    try:
        feedback = Feedback.get(Feedback.id == feedback_id)
    except Exception as e:
        return make_response_json(404, "不存在此反馈")
    datas = feedback.__data__
    print(datas)
    datas.pop("id")
    datas["publish_time"] = str(datas["publish_time"])
    return make_response_json(200, "此反馈信息如下", data=datas)


@api_blue.route("/reply_feedback", methods=["PUT"])
def reply_feedback():
    if not current_user.is_authenticated or current_user.state != User_state.Admin.value:
        return make_response_json(401, "用户无权访问")
    data = request.get_json()
    if "reply_content" not in data:
        return make_response_json(400, "请求格式错误")
    try:
        feedback_id = int(data["feedback_id"])
    except Exception as e:
        return make_response_json(400, "请求格式错误")
    try:
        feedback = Feedback.get(Feedback.id == feedback_id)
    except Exception as e:
        return make_response_json(404, "不存在此反馈")
    feedback.reply_content = data["reply_content"]
    feedback.state = Feedback_state.Replied.value
    feedback.save()
    send_message(SYS_ADMIN_NO, feedback.user_id.id,f'管理员已回复你的反馈，回复内容：\n{data["reply_content"]}')
    return make_response_json(200, "回复完成")
