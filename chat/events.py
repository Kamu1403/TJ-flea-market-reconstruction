#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
from chat.models import Room,Message,Recent_Chat_List
from app import socketio
from app import database

import json

@socketio.on('joined', namespace='/chat')
def joined(message):
    if database.is_closed():
        database.connect()
        
    sender = str(current_user.id) 
    roomid = message['room']
    
    join_room(sender)
    """
    加入自身房间
    读取二者的历史记录
    """
    
    for user in Message.select().where(Message.room_id==roomid):
        
        emit('message', {'msg': str(user.sender_id) + ':' + user.msg_content,
                         'time':str(user.msg_time),'type':user.msg_type},
         room=sender)

    #Room表中标记用户在线
    Room.update(room_state=Room.room_state+1).where(Room.room_id==roomid).execute()
    print("+")
    
    #将最近列表中的未读信息数清空
    Recent_Chat_List.update(unread=0).where(
                Recent_Chat_List.receiver_id==sender
                and Recent_Chat_List.sender_id==message['receiver']).execute()
    
    #将该房间内的所有未读信息全部置为已读
    Message.update(msg_read=1).where(Message.room_id==roomid).execute()
    
    emit('status', {'msg': sender+ ' has entered the room.','time':message['time']},
         room=sender)
    '''进入提醒可删除'''
    
    if not database.is_closed():
        database.close()


@socketio.on('text', namespace='/chat')
def text(message):
    if database.is_closed():
        database.connect()
            
    sender = str(current_user.id)
    
    roomid = message['room']

    state=Room.get_or_none(Room.room_id==roomid)
    
    read=0
    if (state==None):
        pass
    elif state.room_state==2:
        read=1
    
    if read==0:
        if Recent_Chat_List.get_or_none(receiver_id=message['receiver'])==None:
            Recent_Chat_List.insert(
            receiver_id=message['receiver'],
            sender_id=sender,
            last_time=message['time'],
            last_msg=message['msg'],
            unread=1).execute()
        else:
            Recent_Chat_List.update(
            last_time=message['time'],
            last_msg=message['msg'],
            unread=Recent_Chat_List.unread+1).where(Recent_Chat_List.receiver_id==message['receiver'] and Recent_Chat_List.sender_id==sender).execute()
        
    Message.create(
                msg_time=message['time'],
                room_id=roomid,
                sender_id=sender,
                msg_type=message['type'],
                msg_content=message['msg'],
                msg_read=read)
    
    Room.update(last_message=message['msg']).where(Room.room_id==roomid).execute()
    
    emit('message', {'msg': sender + ':' + message['msg'],'time':message['time'],'type':message['type']},
         room=sender)
    if not database.is_closed():
        database.close()

@socketio.on('left', namespace='/chat')
def left(message):
    if database.is_closed():
        database.connect()
    sender = str(current_user.id)
    
    roomid = message['room']

    leave_room(sender)
    Room.update(room_state=Room.room_state-1).where(Room.room_id==roomid).execute()
    print("-")
    
    emit('status', {'msg': sender + ' has left the room.'},
         room=sender)
    '''退出提醒可删除'''
    if not database.is_closed():
        database.close()
