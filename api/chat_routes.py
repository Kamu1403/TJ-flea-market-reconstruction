from api.utils import *
from api import api_blue
from chat import chat_blue
from chat.models import Room,Recent_Chat_List,Meet_List,Message
from PIL import Image
from hashlib import md5

def createPath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)

def save_pic(path,data):
    '''
    传入request.files.get('something') (data类型为werkzeug.filestorage)
    将图片读取后按WEBP转换，保存入临时图床文件夹
    最后返回{400，失败}或{200，成功，md5(str)}
    '''
    try:
        #os.path.join(item_blue.static_folder, f'resource/temp')
        #或
        #url_for('item.static', filename=f'resource/item_pic/{item_id}/[head|pic]')
        curpath = path
        createPath(curpath)

        path_name = os.path.join(curpath, data.filename)
        createPath(curpath)
        data.save(path_name)
        img = Image.open(path_name)
        w, h = img.size
        ratio = max(w, h) / 1920
        if ratio > 1:
            img = img.resize((int(w / ratio), int(h / ratio)))
        ratio = 250 / min(w, h)
        if ratio > 1:
            img = img.resize((int(w * ratio), int(h * ratio)))
        md5_str = md5(img.tobytes()).hexdigest()
        os.remove(path_name)

        path_name_new = os.path.join(curpath, f'{md5_str}')
        img.save(path_name_new, 'WEBP')
        img = Image.open(path_name_new)
        md5_str = md5(img.tobytes()).hexdigest()
        os.remove(path_name_new)

        path_name_new = os.path.join(curpath, f'{md5_str}')
        #if os.path.exists(path_name_new):
        #    return make_response_json(400, f"上传图片失败：请勿重复上传图片")
        img.save(path_name_new, 'WEBP')
    except Exception as e:
        print(e)
        return make_response_json(400, f"上传图片失败：文件格式错误或损坏")
    else:
        return make_response_json(200, "上传图片成功", md5_str)

@api_blue.route("/post_chat_pic", methods=["POST"])
def post_chat_pic():
    if not current_user.is_authenticated:
        return make_response_json(401, "当前用户未登录")
    sender=request.values['sender']
    receiver=request.values['receiver']
    room = request.values['room']
    path= os.path.join(chat_blue.static_folder, f'resource/temp/'+room)
    ret=save_pic(path,request.files.get('file'))
    statusCode=json.loads(ret.data)['statusCode']
    if (statusCode==200):
        md5_str=json.loads(ret.data)['data']
        #写入数据库
        send_message(sender,receiver,md5_str,1)
    return ret


@api_blue.route('/get_message_cnt',methods=['GET'])
def get_message_cnt():
    if (current_user.is_authenticated):
        user=str(current_user.id)
        unread=0
        for chat in Recent_Chat_List.select().where(Recent_Chat_List.receiver_id==user):
            unread+=chat.unread
        res={'unread':unread}
        
        #send_message("80000000",user,"获取成功",'text')
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
            type=roomid.msg_type
            res[m]={'sender':sender,'last_msg':msg,'type':type}
        return make_response_json(200, "获取最后消息成功",res)
    else:
        return make_response_json(401, "当前用户未登录")
    
@api_blue.route('/del_meet',methods=['DELETE'])
def del_meet():
    if (current_user.is_authenticated):
        suser=str(current_user.id)
        del_user=str(request.get_json()['user_id'])
        user,created=Meet_List.get_or_create(user_id=suser)
        meet_list={}
        if created:
            meet_list[user]=[]
        else:
            meet_list=user.meet_list
            meet_list[suser].remove(del_user)
        Meet_List.update(meet_list=meet_list).where(Meet_List.user_id==suser).execute()
        return make_response_json(200, "获取会话列表成功")
    else:
        return make_response_json(401, "当前用户未登录")