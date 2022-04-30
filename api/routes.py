#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api import api_blue
from flask import request
from flask import make_response, request, jsonify

#{ success: boolean, statusCode: int, message: string, data: object }

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

#查
@api_blue.route('/get', methods=['GET'])
def get_api():
    """
    输入
    {
        table_name:name,
        requirment:{
                id:id,
                name:id,
                ...
            },
        target:email
    }

    输出
    {
        success:True,
        status:200,
        message:"good",
        data:[
            {
                email:email,
                ...
            },
            {
                email:email,
                ...
            },
            ...
        ]
    }
    """
    return 'get!'
