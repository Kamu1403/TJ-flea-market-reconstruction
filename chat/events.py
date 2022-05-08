#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from chat.models import Room,Message,Recent_Chat_List
from app import socketio
from app import database

@socketio.on('joined', namespace='/chat')
def joined(message):
    if database.is_closed():
        database.connect()
    """
    加入自身房间
    读取二者的历史记录
    """
    
    sender = str(current_user.id) 

    roomid = message['room']

    '''
    sender用户的id作为roomid的键 即进入自己的room
    第一次建立 连接形成的sid作为roomid的值 
    '''
    Room.update(room_state=Room.room_state+1).where(Room.room_id==roomid).execute()
    
    join_room(sender)
    emit('status', {'msg': sender+ ' has entered the room.','time':message['time']},
         room=sender)
    '''进入提醒可删除'''
    
    '''
    读取历史记录
    
    '''
    if not database.is_closed():
        database.close()


@socketio.on('text', namespace='/chat')
def text(message):
    if database.is_closed():
        database.connect()
            
    sender = str(current_user.id)
    
    roomid = message['room']


    state=Room.get_or_none(Room.room_id==roomid)
    read=1 if state.room_state==2 else 0
    
    Message.create(
                msg_time=message['time'],
                room_id=roomid,
                sender_id=sender,
                msg_type=message['type'],
                msg_content=message['msg'],
                msg_read=read)
    
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
    user_list[sender]=None  #退出房间 未进入房间时 将userlist中对应的roomid置为空
    
    leave_room(room_dict[sender])
    Room.update(room_state=Room.room_state-1).where(Room.room_id==roomid).execute()
    emit('status', {'msg': sender + ' has left the room.'},
         room=sender)
    '''退出提醒可删除'''
    if not database.is_closed():
        database.close()
