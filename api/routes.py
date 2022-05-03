#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_login import current_user
from api import api_blue
from flask import make_response, request, jsonify
#enum
from user.models import User_state
from admin.models import Feedback_kind,Feedback_state
from order.models import Order_state
#model
from user.models import User
from admin.models import Feedback,User_Management
from order.models import Contact,Review,Order,Order_State_Item,Order_Item
from item.models import Goods,Want,HistoryGoods,HistoryWant,FavorGoods,FavorWant


#返回值规范
#{ success: boolean, statusCode: int, message: string, data: object }
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

def GetUserDict(i)->dict:
    user={}
    user['id']=i.id
    user['username']=i.username
    user['email']=i.email
    user['state']=i.state
    user['score']=i.score
    user['telephone']=i.telephone
    user['wechat']=i.wechat
    user['qq_number']=i.qq_number
    user['campus_branch']=i.campus_branch
    user['dormitory']=i.dormitory
    user['gender']=i.gender
    user['name_is_published']=i.name_is_published
    if i.name_is_published==True:
        user['name']=i.name
    else:
        user['name']='保密'
    user['major_is_published']=i.major_is_published
    if i.major_is_published==True:
        user['major']=i.major
    else:
        user['major']='保密'
    return user

#管理员获取所有用户信息
@api_blue.route('/getalluser',methods=['GET'])
def getalluser():
    res={'success': True, 'statusCode': 200, 'message': '','data':{}}
    data_list=[]
    
    #在APIFOX测试运行时current_user未经认证，故注释下面一行，正式运行时取消注释
    #if current_user.state==User_state.Admin.value:#如果当前用户是管理员
    if True:
        users=User.select().where(User.state!=User_state.Admin.value)
        for i in users:
            user_dic=GetUserDict(i)
            data_list.append(user_dic)
        res['data']=data_list

        if len(data_list)>0:
            res['message']="所有用户信息获取成功"
        else:
            res['message']="未找到对应用户信息"
            res['statusCode']=404
            res['success']=False

    else:#非管理员
        res['message']="非管理员无此权限"
        res['statusCode']=401
        res['success']=False

    return make_response(jsonify(res))



#增
@api_blue.route('/post', methods=['POST'])
def post_api():
    """
    输入
    {
        table_name:name,
        [
            {
                id:id,
                name:id,
                ...
            },
            {
                id:id,
                name:id,
                ...
            },
            ...
        ]
    }

    输出
    {
        success:True,
        status:200,
        message:"good"
    }
    """
    #if request.method == 'POST':
    #    table_name = request.form.get("table_name")

    resp= {
        'success':True,
        'status':200,
        'message':"good"
    }
    print(jsonify(resp))
    return make_response(jsonify(resp))

#删
@api_blue.route("/delete", methods=['DELETE'])
def delete_api():
    """
    输入
    {
        table_name:name,
        requirment:{
                id:id,
                name:name,
                ...
            },

    }

    输出
    {
        success:True,
        status:200,
        message:"good"
    }
    """
    resp= {
        'success':True,
        'status':200,
        'message':"good"
    }
    return make_response(jsonify(resp))

#改
@api_blue.route('/put', methods=['PUT'])
def put_api():
    """
    输入
    {
        table_name:name,
        newdata:[
            {
                id:id,
                name:id,
                ...
            },
            {
                id:id,
                name:id,
                ...
            },
            ...
        ]
    }

    输出
    {
        success:True,
        status:200,
        message:"good"
    }
    """
    resp= {
        'success':True,
        'status':200,
        'message':"good"
    }
    return make_response(jsonify(resp))

