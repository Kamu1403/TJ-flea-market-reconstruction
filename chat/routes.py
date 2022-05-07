from flask import redirect, url_for, render_template, request
from flask_login import current_user
from chat import chat_blue
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
@chat_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('chat.index'))  # 重定向到/user/index


@chat_blue.route('/index', methods=['GET', 'POST'])
def index():
    #显示左侧聊天列表，右侧聊天框空白
    return render_template('chat.html',name=current_user,room="")

#进入聊天室
@chat_blue.route('/<opt_userid>')
def chat(opt_userid:int):
    #显示左侧聊天列表，右侧聊天框根据opt_user渲染
    return render_template('chat.html', name=current_user, room=opt_userid)
