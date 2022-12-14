#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
from chat.models import Room,Message,Recent_Chat_List,Meet_List
from app import socketio
from app import database



import json

def create_or_update_meet_list(sender,receiver):
    user,created=Meet_List.get_or_create(user_id=sender)
    meet_list={}
    if created:
        meet_list[sender]=[receiver]
    else:
        meet_list=user.meet_list
        if receiver not in meet_list[sender]:
            meet_list[sender].append(receiver)
    Meet_List.update(meet_list=meet_list).where(Meet_List.user_id==sender).execute()


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
        emit('message', {'sender':str(user.sender_id), 'msg':user.msg_content,
                         'other_user':message['receiver'],
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
    
    '''emit('status', {'msg': sender+ ' has entered the room.','time':message['time']},
         room=sender)
    进入提醒可删除'''
    
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
            
            Recent_Chat_List.update(
            last_time=message['time'],
            last_msg=message['msg'],).where(Recent_Chat_List.receiver_id==sender and Recent_Chat_List.sender_id==message['receiver']).execute()
        
    Message.create(
                msg_time=message['time'],
                room_id=roomid,
                sender_id=sender,
                msg_type=message['type'],
                msg_content=message['msg'],
                msg_read=read)
    
    Room.update(last_message=message['msg'],last_sender_id=sender,msg_type=message['type']).where(Room.room_id==roomid).execute()
    create_or_update_meet_list(sender,message['receiver'])
    create_or_update_meet_list(message['receiver'],sender)
    
    emit('message', {'sender':sender,
                     'msg':message['msg'],
                     'other_user':message['receiver'],
                     'time':message['time'],
                     'type':message['type']},
         room=sender)
    
    if (read==1):
        emit('message', {'sender':sender,
                        'msg':message['msg'],
                        'other_user':sender,
                        'time':message['time'],
                        'type':message['type']},
            room=message['receiver'])
    else:
        emit('notice', {'sender':sender,
                        'msg':message['msg'],
                        'other_user':sender,
                        'time':message['time'],
                        'type':message['type']},
            room=message['receiver'])

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
    
    '''emit('status', {'msg': sender + ' has left the room.'},
         room=sender)
    退出提醒可删除'''
    if not database.is_closed():
        database.close()
