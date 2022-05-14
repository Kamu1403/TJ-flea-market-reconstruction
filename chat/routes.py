from flask import redirect, url_for, render_template, request,flash
from flask_login import current_user
from chat import chat_blue
from flask_socketio import leave_room
from flask import make_response, request, jsonify
from chat.models import Room,Recent_Chat_List
from api.utils import *
from app import database

@chat_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()
        
@chat_blue.teardown_request
def teardown_request(exc):#exc必须写上
    if not database.is_closed():
        database.close()

#聊天室初始
@chat_blue.route("", methods=['GET', 'POST'])
@chat_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('chat.index'))  # 重定向到/user/index


@chat_blue.route('/index', methods=['GET', 'POST'])
def index():
    #显示左侧聊天列表，右侧聊天框空白
    if (current_user.is_authenticated):
        return render_template('chat.html')
    else:
        return redirect(url_for('login'))  # 重定向到/login

#进入聊天室
@chat_blue.route('/<opt_userid>')
def chat(opt_userid:int):
    #显示左侧聊天列表，右侧聊天框根据opt_user渲染
    if (current_user.is_authenticated):
        sender=str(current_user.id)
        receiver=opt_userid
        room = sender + '-' + receiver
        reroom = receiver + '-' + sender
        #查询是否存在该聊天,发送接收双方此时共享一个聊天室(聊天记录)
        
        if (sender!=receiver):
            roomid = Room.get_or_none(Room.room_id==room)
            reroomid=Room.get_or_none(Room.room_id==reroom)
            if (roomid==None and reroomid==None):
                Room.create(room_id=room)
            elif reroomid!=None:
                room=reroom
                
        return render_template('chat.html',sender=sender,receiver=receiver,room=room)
    else:
        return redirect(url_for('login'))  # 重定向到/login

@chat_blue.route('/close',methods=['POST','GET'])
def close():
    room=request.data.decode()
    sender=str(current_user.id)
    
    print("-")
    Room.update(room_state=Room.room_state-1).where(Room.room_id==room).execute()
    
    
    print("close!")
    return jsonify('status:200')

@chat_blue.route('/message_cnt',methods=['POST','GET'])
def message_cnt():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        unread=0
        for chat in Recent_Chat_List.select().where(Recent_Chat_List.receiver_id==user):
            unread+=chat.unread
        return unread
    else:
        return make_response_json(400, "当前用户未登录")