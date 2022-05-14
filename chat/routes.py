from flask import redirect, url_for, render_template, request
from flask_login import current_user
from chat import chat_blue
from flask_socketio import leave_room
from flask import make_response, request, jsonify
from chat.models import Room,Recent_Chat_List
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
        tag1,tag2=0,0
        #查询是否存在该聊天,发送接收双方此时共享一个聊天室(聊天记录)
        try:
            roomid = Room.get(Room.room_id==room)
        except:
            tag1=1
        
        try:
            roomid = Room.get(Room.room_id==reroom)
        except:
            tag2=1

        if (tag1 and tag2):
            Room.create(room_id=room)
        elif tag1:
            room=reroom
        return render_template('chat.html',receiver=receiver,room=room)
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