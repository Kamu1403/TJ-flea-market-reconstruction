from api.utils import *
from api import api_blue
from chat.models import Room,Recent_Chat_List

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
    
@api_blue.route('/get_chat_list',methods=['GET'])
def get_chat_list():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        unread=0
        for chat in Recent_Chat_List.select().where(Recent_Chat_List.receiver_id==user):
            unread+=chat.unread
        res={'unread':unread}
        return make_response_json(200, "获取未读条数成功",res)
    else:
        return make_response_json(401, "当前用户未登录")