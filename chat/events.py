#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app import database

user_list={}    #在线用户--房间表
room_dict = {}  #用户--房间表 user-sid 一对一
meet={}         
'''聊天记录表 
改为从数据库进行读取
'''


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    sender = current_user
    receiver = message['room']
    
    room=sender
    '''
    sender用户的id作为roomid的键 即进入自己的room
    第一次建立 连接形成的sid作为roomid的值 
    '''
    sid = request.sid
    if (room not in room_dict):
        room_dict[room] = sid

    join_room(room_dict[room])
    emit('status', {'msg': current_user+ ' has entered the room.','time':message['time']},
         room=room_dict[room])
    '''进入提醒可删除'''
    
    user_list[sender]=receiver
    
    '''
    unread_msg_count=redis_msg.get_redis_one(sender,receiver)#注意发送接收需要反过来 因为此时的sender实际上是未读消息的receiver
    
    if unread_msg_count!=0:
        for chat in meet[room_dict[room]][-unread_msg_count:]:
            emit('message', {'msg': chat['sender'] + ':' + chat['msg'],'time':chat['time']},
            to=room_dict[room])
    
    进入房间后在线用户表更新 查询redis是否有未读信息
    实际上项目无需如此复杂  因为每次进入room都是将整个聊天记录中最后几条发送过去 
    不管其离线期间收到过几条 
    redis应该只缓存条数用以提醒用户
    问题1:进入房间后未读信息可以显示 但是在原发送方会显示两条 如何隔绝双方？
    1.前端只通过读取json显示聊天 而非直接前端发送自动更新
    2.修改数据结构 每个人只有自己单独的房间 发送到该房间的信息按sender分开 √
    问题2:修改数据结构后 在同一个房间来自不同发送方的消息都能被看见 如何隔绝各方？
    1.修改后台逻辑 每个人登录后进入自己所在的房间 发送信息就是送到指定房间 因此meet需要修改
    '''
    

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    sender = session.get('name')
    receiver = session.get('receiver')

    room=sender
    
    chats = {   "msg": message['msg'],
                "sender": sender,
                "receiver": receiver,
                "time":message['time'],
                'type':message['type']
                    }
    if (room_dict[sender] not in meet):
        meet[room_dict[sender]]=[chats]
        meet[room_dict[receiver]]=[chats]
    else :
        meet[room_dict[sender]].append(chats)
        meet[room_dict[receiver]].append(chats)
        '''
        前置条件：双方都注册过 room_dict中有其记录
        应该使用mysql 消息存储 但鉴于数据结构还未能确定 暂不实现
        无论双方是否都在线 发送成功的消息一定更要存储在数据库中
        update:双方的meet—room中都要存储 方便后续取用
        '''           
    print(user_list)
    if (receiver not in user_list or user_list[receiver]!=sender):
        '''
        redis,离线消息缓存 有以下几种可能
        1.用户未注册 实际情况并不发生 在开发过程中特殊处理
        2.用户离线 user_list对应为None
        3.双方不在同一个页面
        
        redis_msg.set_redis(receiver,sender)
        '''
        pass
    else:
        '''
        对方在线就立即发送？？？？
        
        receiver应该是跟在/chat路由之后的参数 并根据该参数显示不同的页面
        而左侧的提醒栏提醒的是未读通知 因此 如果对方的receiver并不是我 那我就不应该emit
        
        或者 我emit之后在前端进行确认 发来的消息里receiver是不是我想要看到的！！！ 似乎可行
        如此一来 命名空间需要修改为receive和send 不能都用message了
        
        再或者 把userlist数据结构修改一下？把userid-->roomid修改成sender-->receiver 这样好像更简单
        '''
        emit('message', {'msg': session.get('name') + ':' + message['msg'],'time':message['time'],'type':message['type']},
        room=room_dict[receiver])       
         
    emit('message', {'msg': session.get('name') + ':' + message['msg'],'time':message['time'],'type':message['type']},
         room=room_dict[sender])#此处应该为前端自动读取变化 减少后端压力


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    sender = session.get('name')
    receiver = session.get('receiver')
    room =sender
    user_list[sender]=None  #退出房间 未进入房间时 将userlist中对应的roomid置为空
    
    leave_room(room_dict[sender])
    emit('status', {'msg': session.get('name') + ' has left the room.'},
         room=room_dict[sender])
    '''退出提醒可删除'''
