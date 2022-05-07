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

    if User.table_exists:
        User.drop_table()
        
    if Room.table_exists:
        Room.drop_table()
    if Recent_Chat_List.table_exists:
        Room.drop_table()
    if Message.table_exists:
        Message.drop_table()

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
    Room.create_table()
    Message.create_table()
    
def fake_data():#填一些假数据进去
    pass


def init_database(drop_database:bool):
    if drop_database==True:
        drop_tables()
        create_tables()
        fake_data()
