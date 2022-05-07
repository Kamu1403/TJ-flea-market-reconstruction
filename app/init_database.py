#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#model
from user.models import User
from admin.models import Feedback,User_Management
from order.models import Contact,Review,Order,Order_State_Item,Order_Item
from item.models import Goods,Want,HistoryGoods,HistoryWant,FavorGoods,FavorWant
from chat.models import Room,Message,Recent_Chat_List

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

    if FavorWant.table_exists:
        FavorWant.drop_table()
    if FavorGoods.table_exists:
        FavorGoods.drop_table()
    if HistoryWant.table_exists:
        HistoryWant.drop_table()
    if HistoryGoods.table_exists:
        HistoryGoods.drop_table()
    if Want.table_exists:
        Want.drop_table()
    if Goods.table_exists:
        Goods.drop_table()

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
    
    if User.table_exists:
        User.drop_table()
        
def create_tables():
    User.create_table()

    Feedback.create_table()
    User_Management.create_table()

    Goods.create_table()
    Want.create_table()
    HistoryGoods.create_table()
    HistoryWant.create_table()
    FavorGoods.create_table()
    FavorWant.create_table()

    Contact.create_table()
    Review.create_table()
    Order.create_table()
    Order_State_Item.create_table()
    Order_Item.create_table()

    Room.create_table()
    Recent_Chat_List.create_table()
    Message.create_table()
    

from datetime import datetime
from werkzeug.security import generate_password_hash
def fake_data():#填一些假数据进去
    User.create(id=1951705,username="高曾谊",state=1,#管理员
            password_hash=generate_password_hash("1951705"),
            email=str(1951705)+"@tongji.edu.cn")
    User.create(id=1950084,username="陈泓仰",state=1,
            password_hash=generate_password_hash("1950084"),
            email=str(1950084)+"@tongji.edu.cn")
    User.create(id=1951566,username="贾仁军",
            password_hash=generate_password_hash("1951566"),
            email=str(1951566)+"@tongji.edu.cn")
    User.create(id=1953493,username="程森",state=-1,#被封号
            password_hash=generate_password_hash("1953493"),
            email=str(1953493)+"@tongji.edu.cn")

    #反馈
    Feedback.create(user_id=1951705,feedback_content="哈哈哈哈")
    Feedback.create(user_id=1953493,state=-1,feedback_content="有bug啊",reply_content="bug在哪?")
    
    #封号 程森被封到2022.6.1
    User_Management.create(user_id=1953493,ban_reason="恶意利用网站bug",ban_time=datetime(2022,6,1))

    #商品、悬赏
    Goods.create(name="苹果",publisher_id=1951705,price=1.11,tag="食物",pic_num=0)
    Goods.create(name="方便面",publisher_id=1950084,price=3.33,shelved_num=999)
    Goods.create(name="肉",publisher_id=1950084,price=10,shelved_num=999)
    Want.create(name="沈坚作业",publisher_id=1951705,price=0.01,tag="作业",description="求帮忙写sj作业")
    Want.create(name="耳机",publisher_id=1953493,price=300,tag="电子用品",description="求耳机一副")
    
    #浏览 收藏
    HistoryGoods.create(visitor_id=1951705,goods_id=2)
    HistoryGoods.create(visitor_id=1951566,goods_id=2)
    HistoryGoods.create(visitor_id=1950084,goods_id=1)
    FavorGoods.create(collector_id=1951705,goods_id=2)
    FavorGoods.create(collector_id=1951566,goods_id=2)
    FavorGoods.create(collector_id=1950084,goods_id=1)
    HistoryWant.create(visitor_id=1951705,want_id=2)
    HistoryWant.create(visitor_id=1951566,want_id=2)
    HistoryWant.create(visitor_id=1950084,want_id=1)
    FavorWant.create(collector_id=1951705,want_id=2)
    FavorWant.create(collector_id=1951566,want_id=2)
    FavorWant.create(collector_id=1950084,want_id=1)
    

    Contact.create(user_id=1951705,name="高曾谊",telephone="+86 111111111",addr="xxx")
    Contact.create(user_id=1950084,name="陈泓仰",telephone="+86 1112111111",addr="xyxx")
    Contact.create(user_id=1953493,name="程森",telephone="+86 1111111131",addr="zzzx")
    Contact.create(user_id=1951566,name="贾仁军",telephone="+86 11123111131",addr="kkzx")

    Review.create(user_id=1951705,feedback_content="默认好评")
    Review.create(user_id=1950084,feedback_content="默认好评")
    Review.create(user_id=1953493,feedback_content="默认好评")
    Review.create(user_id=1951566,feedback_content="默认好评")

    Order.create(user_id=1951705,op_user_id=1951566,contact_id=4,payment=1.11,state=2,end_time=datetime.utcnow())
    Order.create(user_id=1951705,op_user_id=1953493,contact_id=3,payment=0.01,state=-1,close_time=datetime.utcnow(),note="我来帮你写sj！")
    Order.create(user_id=1950084,op_user_id=1951566,contact_id=4,payment=59.99,state=0)#5份肉 3份方便面

    Order_State_Item.create(order_id=1,user_review_id=1,op_user_review_id=4)
    Order_State_Item.create(order_id=2,cancel_user=1950084,cancel_reason="沈坚作业不能作为悬赏！")
    Order_State_Item.create(order_id=3)
    
    #订单3中包含 5份肉 3份方便面
    Order_Item.create(order_id=3,quantity=3,kind=0,goods_id=2)#方便面
    Order_Item.create(order_id=3,quantity=5,kind=0,goods_id=3)#肉

    #订单2中包含 1份沈坚作业
    Order_Item.create(order_id=2,quantity=1,kind=1,want_id=1)#沈坚作业

    #订单1中包含 1份苹果
    Order_Item.create(order_id=1,quantity=1,kind=0,goods_id=1)#苹果



def init_database(drop_database:bool):
    if drop_database==True:
        drop_tables()
        create_tables()
        fake_data()
