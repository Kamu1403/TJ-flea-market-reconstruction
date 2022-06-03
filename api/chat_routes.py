from api.utils import *
from api import api_blue
from chat.models import Room,Recent_Chat_List,Meet_List

@api_blue.route('/get_message_cnt',methods=['GET'])
def get_message_cnt():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        unread=0
        for chat in Recent_Chat_List.select().where(Recent_Chat_List.receiver_id==user):
            unread+=chat.unread
        res={'unread':unread}
        return make_response_json(200, "获取未读条数成功",res)
    else:
        return make_response_json(401, "当前用户未登录")
    
@api_blue.route('/get_meet_list',methods=['GET'])
def get_meet_list():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        meet=Meet_List.get_or_none(Meet_List.user_id==user)
        if meet==None:
            meet_list=""
        else:
            meet_list=meet.meet_list[user]
        res={'meet_list':meet_list}
        return make_response_json(200, "获取会话列表成功",res)
    else:
        return make_response_json(401, "当前用户未登录")
    
@api_blue.route('/get_last_msg',methods=['GET'])
def get_last_msg():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        meet=Meet_List.get_or_none(Meet_List.user_id==user)
        if meet==None:
            meet_list=""
        else:
            meet_list=meet.meet_list[user]
        res={}
        for m in meet_list:
            room=user+'-'+m
            reroom=m+'-'+user
            roomid = Room.get_or_none(Room.room_id==room)
            reroomid=Room.get_or_none(Room.room_id==reroom)
            if roomid==None:
                roomid=reroomid
            msg=roomid.last_message
            sender=roomid.last_sender_id.id
            res[m]={'sender':sender,'last_msg':msg}
        return make_response_json(200, "获取最后消息成功",res)
    else:
        return make_response_json(401, "当前用户未登录")