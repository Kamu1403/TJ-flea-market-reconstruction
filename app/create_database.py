#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pymysql
def create_database(database_name="tj_market",password='tj_market',user="root"):
    """python + pymysql 创建数据库"""
    
    # 创建连接
    conn = pymysql.connect(host='localhost',
                        user=user,
                        password=password,
                        charset='utf8mb4')
    # 创建游标
    cursor = conn.cursor()
    
    # 创建数据库的sql(如果数据库存在就不创建，防止异常)
    sql = "DROP DATABASE IF EXISTS "+database_name
    # 执行删除数据库的sql
    cursor.execute(sql)

    sql = "CREATE DATABASE IF NOT EXISTS "+database_name
    # 执行创建数据库的sql
    cursor.execute(sql)
