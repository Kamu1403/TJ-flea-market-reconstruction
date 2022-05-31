#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#model
from user.models import User
from admin.models import Feedback, User_Management
from order.models import Contact, Review, Order, Order_State_Item, Order_Item
from item.models import Item, History, Favor
from chat.models import Room, Message, Recent_Chat_List, Meet_List
from datetime import timedelta

def drop_tables():
    if Order_Item.table_exists:
        Order_Item.drop_table()
    if Order_State_Item.table_exists:
        Order_State_Item.drop_table()
    if Order.table_exists:
        Order.drop_table()
    if Review.table_exists:
        Review.drop_table()
    if Contact.table_exists:
        Contact.drop_table()

    if Favor.table_exists:
        Favor.drop_table()
    if History.table_exists:
        History.drop_table()
    if Item.table_exists:
        Item.drop_table()

    if User_Management.table_exists:
        User_Management.drop_table()
    if Feedback.table_exists:
        Feedback.drop_table()

    if Recent_Chat_List.table_exists:
        Recent_Chat_List.drop_table()
    if Message.table_exists:
        Message.drop_table()
    if Room.table_exists:
        Room.drop_table()
    if Meet_List.table_exists:
        Meet_List.drop_table()

    if User.table_exists:
        User.drop_table()


def create_tables():
    User.create_table()

    Feedback.create_table()
    User_Management.create_table()

    Item.create_table()
    History.create_table()
    Favor.create_table()

    Contact.create_table()
    Review.create_table()
    Order.create_table()
    Order_State_Item.create_table()
    Order_Item.create_table()

    Room.create_table()
    Recent_Chat_List.create_table()
    Message.create_table()
    Meet_List.create_table()


from datetime import datetime
from werkzeug.security import generate_password_hash


def fake_data():  #填一些假数据进去
    User.create(id=80000000,
                username="系统管理员",
                state=1,
                password_hash=generate_password_hash("admin"),
                email="admin@admin.cn")
    User.create(
        id=1951705,
        user_no="1951705",
        username="高曾谊",name="高曾谊",
        state=1,  #管理员
        password_hash=generate_password_hash("1951705"),
        email=str(1951705) + "@tongji.edu.cn")
    User.create(id=1950084,
                user_no="1950084",
                username="陈泓仰",name="陈泓仰",
                state=1,
                password_hash=generate_password_hash("1950084"),
                email=str(1950084) + "@tongji.edu.cn")
    User.create(id=1951566,
                user_no="1951566",
                username="贾仁军",name="贾仁军",
                password_hash=generate_password_hash("1951566"),
                email=str(1951566) + "@tongji.edu.cn")
    User.create(
        id=1953493,
        user_no="1953493",
        username="程森",
        state=-1,  #被封号
        password_hash=generate_password_hash("1953493"),
        email=str(1953493) + "@tongji.edu.cn")

    User.create(id=1952219,
                user_no="1952219",
                username="彭斐然",
                password_hash=generate_password_hash("1952219"),
                email=str(1952219) + "@tongji.edu.cn")
    User.create(id=1951859,
                user_no="1951859",
                username="杨可盈",
                password_hash=generate_password_hash("1951859"),
                email=str(1951859) + "@tongji.edu.cn")

    #反馈
    Feedback.create(user_id=1951705, feedback_content="哈哈哈哈")
    Feedback.create(user_id=1953493,
                    state=-1,
                    feedback_content="有bug啊",
                    reply_content="bug在哪?")

    #封号 程森被封到2022.6.1
    User_Management.create(user_id=1953493,
                           ban_reason="恶意利用网站bug",
                           ban_time=datetime(2022, 6, 1))

    #商品、悬赏  0是商品--123，1是悬赏--45
    Item.create(id=1,
                name="苹果",
                user_id=1951705,
                shelved_num=999,
                locked_num=10,
                price=1.11,
                tag="食物",
                type=0)
    Item.create(id=2,
                name="方便面",
                user_id=1950084,
                price=3.33,
                shelved_num=999,
                locked_num=10,
                type=0)
    Item.create(id=3,
                name="肉",
                user_id=1950084,
                price=10,
                shelved_num=999,
                locked_num=10,
                type=0)
    Item.create(id=4,
                name="沈坚作业",
                user_id=1951705,
                price=0.01,
                tag="作业",
                description="求帮忙写sj作业",
                type=1)
    Item.create(id=5,
                name="耳机",
                user_id=1953493,
                shelved_num=2,
                locked_num=2,
                price=300,
                tag="电子用品",
                description="求耳机一副",
                type=1)

    Item.create(id=6,
                name="方便面",
                user_id=1951566,
                price=3.33,
                shelved_num=999,
                locked_num=10,
                type=0)

    Item.create(id=7,
                name="方便面",
                user_id=1951566,
                price=2.22,
                shelved_num=0,
                locked_num=10,
                type=0)

    #浏览 收藏
    History.create(user_id=1951705, item_id=2, visit_time=datetime(2022, 4, 1))
    History.create(user_id=1951566, item_id=2)
    History.create(user_id=1950084, item_id=1)
    Favor.create(user_id=1951705, item_id=2)
    Favor.create(user_id=1951566, item_id=3)
    Favor.create(user_id=1950084, item_id=1)

    History.create(user_id=1951705, item_id=5, visit_time=datetime(2022, 4, 3))
    History.create(user_id=1951566, item_id=5)
    History.create(user_id=1950084, item_id=4)
    Favor.create(user_id=1951705, item_id=5)
    Favor.create(user_id=1951566, item_id=5)
    Favor.create(user_id=1950084, item_id=4)
    Contact.create(id=10,
                   user_id=1951705,
                   name="高曾谊",
                   telephone="+86 11111uoiujoij",
                   full_address="address2",
                   default=False)
    Contact.create(id=1,
                   user_id=1951705,
                   name="高曾谊",
                   telephone="+86 111dfasfs11",
                   full_address="address1",
                   default=True)
    Contact.create(id=2,
                   user_id=1950084,
                   name="陈泓仰",
                   telephone="+86 1112111111",
                   full_address="xyxx",
                   default=True)
    Contact.create(id=3,
                   user_id=1953493,
                   name="程森",
                   telephone="+86 1111111131",
                   full_address="zzzx",
                   default=True)
    Contact.create(id=4,
                   user_id=1951566,
                   name="贾仁军",
                   telephone="+86 11123111131",
                   full_address="kkzx",
                   default=True)
    Contact.create(id=5,
                   user_id=1952219,
                   name="彭斐然",
                   telephone="+86 11123111131",
                   full_address="kkzx",
                   default=True)
    Contact.create(id=6,
                   user_id=1951859,
                   name="杨可盈",
                   telephone="+86 11123111131",
                   full_address="kkzx",
                   default=True)

    Review.create(id=1, user_id=1951705, feedback_content="默认好评")
    Review.create(id=2, user_id=1950084, feedback_content="默认好评")
    Review.create(id=3, user_id=1953493, feedback_content="默认好评")
    Review.create(id=4, user_id=1951566, feedback_content="默认好评")

    # 商品
    Order.create(id=1, user_id=1951566, payment=2, state=0,create_time=datetime.now()-timedelta(days=20))
    Order.create(
        id=2,  # 悬赏
        user_id=1953493,
        payment=0.01,
        state=-1,
        confirm_time=datetime.now(),
        note="我来帮你写sj！")
    Order.create(id=3, user_id=1951566, payment=12, state=0)  #3份方便面

    Order.create(id=4, user_id=1951566, payment=10.5, state=1)  #3份方便面

    Order_State_Item.create(order_id=1, user_review_id=1, op_user_review_id=4)
    Order_State_Item.create(order_id=2,
                            cancel_user=1950084,
                            cancel_reason="沈坚作业不能作为悬赏！")
    Order_State_Item.create(order_id=3)
    Order_State_Item.create(order_id=4)
    # 商品
    #订单4中包含 3份方便面
    Order_Item.create(order_id=4, quantity=3, price=3.5, item_id=2)  #方便面

    #订单3中包含 3份方便面
    Order_Item.create(order_id=3, quantity=3, price=4, item_id=2)  #方便面

    #订单2中包含 1份苹果
    Order_Item.create(order_id=2, quantity=1, price=1.5, item_id=1)  #苹果

    #订单1中包含 1份苹果  商品
    Order_Item.create(order_id=1, quantity=1, price=1, item_id=1)  #苹果
    
    Order.create(id=5, user_id=1951566, payment=1.11, state=0)
    Order.create(
        id=6,  # 悬赏
        user_id=1953493,
        payment=300,
        state=1,
        confirm_time=datetime.now(),
        note="我来帮你写sj！")
    Order.create(id=7, user_id=1951566, payment=9.99, state=2)  #3份方便面

    Order.create(id=8, user_id=1951566, payment=9.99, state=2)  #3份方便面

    Order_State_Item.create(order_id=5)
    Order_State_Item.create(order_id=6)
    Order_State_Item.create(order_id=7)
    Order_State_Item.create(order_id=8)


    # 悬赏
    #订单5中包含 3
    Order_Item.create(order_id=5, quantity=3, price=200, item_id=5)  #耳机

    #订单6中包含 1份作业
    Order_Item.create(order_id=6, quantity=1, price=5, item_id=4)  #sj作业

    Order_Item.create(order_id=7, quantity=3, price=3.33, item_id=2)  #方便面

    Order_Item.create(order_id=7, quantity=3, price=3.33, item_id=2)  #方便面


def init_database(drop_database: bool):
    if drop_database == True:
        drop_tables()
        create_tables()
        fake_data()
