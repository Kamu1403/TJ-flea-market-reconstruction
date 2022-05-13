#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state

from .send_verification_mail import send_email


def judge_user_id(user_id: str):
    try:
        user_id = str(user_id).strip()
    except:
        return [400, "账号格式错误"]
    #if '@' not in user_id:
    #    user_id += "@tongji.edu.cn"
    pattern = re.compile(r'^\d{7}@tongji\.edu\.cn$')
    result = pattern.findall(user_id)
    if len(result) > 0:
        return [0, "验证通过"]
    pattern = re.compile(r'@tongji\.edu\.cn$')
    result = pattern.findall(user_id)
    if len(result) > 1:
        return [400, "邮箱账号必须为学号！"]
    return [400, "账号格式错误"]


curpath = os.path.dirname(__file__)
config = os.path.join(
    curpath, 'verify_code.json'
)  # [{"time": int(time.time()), "user_id":str, "code":str}]
if not os.path.exists(config):
    with open(config, "w", encoding="utf-8") as fp:
        print("[]", file=fp)


def save_verify_code(code: List[dict]):
    nowtime = time.time()
    with open(config, "w", encoding="utf-8") as fp:
        json.dump(list(filter(lambda x: nowtime - x["time"] < 900, code)),
                  fp,
                  indent=4,
                  ensure_ascii=False)


def get_verify_code() -> List[dict]:
    with open(config, "r", encoding="utf-8") as fp:
        code = json.load(fp)
    save_verify_code(code)
    return code


def judge_code_frequency(user_id: str) -> list:
    '''
    验证上次发送验证码间隔是否>1min
    :return [statusCode:0|400, message:str]
    '''
    jui = judge_user_id(user_id)
    if jui[0] != 0:
        return jui
    code_list = get_verify_code()
    nowtime = int(time.time())

    for code_record in code_list:
        if code_record["user_id"] == user_id:
            if nowtime - code_record["time"] < 59:
                return [400, "验证码申请过于频繁"]
    return [0, ""]


def judge_code(user_id: str, code: str) -> list:
    '''
    验证验证码是否正确
    :return [statusCode:0|400, message:str]
    '''

    try:
        code = str(code).strip().upper()
    except:
        return [400, "验证码格式错误"]
    if len(code) == 0:
        return [400, "验证码不可为空"]

    jui = judge_user_id(user_id)
    if jui[0] != 0:
        return jui
    #print(code)
    if code == "IEW32DGCBCDZI2B3ELJ7KIAS4HQZMU0M":  # 测试用后门
        return [0, "验证通过"]

    code_list = get_verify_code()
    nowtime = int(time.time())
    code_exist_but_wrong = False
    code_exist_but_outofdate = False
    for code_record in code_list:
        if code_record["user_id"] == user_id:
            if nowtime - code_record["time"] <= 900:
                if code_record["code"] == code:
                    return [0, "验证成功"]
                code_exist_but_wrong = True
            else:
                code_exist_but_outofdate = True

    if code_exist_but_wrong:
        return [400, "验证码错误"]
    if code_exist_but_outofdate:
        return [400, "验证码过期，请重新获取验证码"]
    return [400, "验证码不存在，请先获取验证码"]


def judge_password(password: str):
    if type(password) != str:
        return [400, "密码格式错误"]
    if len(password) < 6:
        return [400, "密码过短"]
    if len(password) > 32:
        return [400, "密码过长"]
    pattern = re.compile(r'[a-zA-Z0-9_-]')
    result = pattern.findall(password)
    if len(result) != len(password):
        return [400, "密码含有非法字符"]
    return [0, "验证通过"]


import string


def create_string_number(n):
    """
    生成一串指定位数的字符+数组混合的字符串
    """
    m = random.randint(1, n)
    a = "".join([str(random.randint(0, 9)) for _ in range(m)])
    b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
    return ''.join(random.sample(list(a + b), n))


@api_blue.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    user_id = request.form.get('email')
    jcf = judge_code_frequency(user_id)
    if jcf[0] != 0:
        return make_response_json(quick_response=jcf)
    verification_code = create_string_number(6)
    ret = send_email(
        "同济跳蚤市场 注册验证码", [user_id],
        f'您的注册验证码为：{verification_code}。有效期为15分钟。\n此邮件为系统自动发出，请勿回复。')

    code_list = get_verify_code()
    code_list.append({
        "time": int(time.time()),
        "user_id": user_id,
        "code": verification_code.upper()
    })
    save_verify_code(code_list)
    if ret["status"] == False:
        return make_response_json(400, "验证码邮件发送失败，请重试或联系网站管理员。")
    retcode = 200
    try:
        User.get(User.email == user_id)
    except:
        retcode = 201
    return make_response_json(retcode, "验证码发送成功")


def _login(user_id, password=None):
    try:
        user = User.get(User.email == user_id)  # 此处还可以添加判断用户是否时管理员
    except:
        return make_response_json(400, "账号不存在")

    if password != None:
        if not user.check_password(password):
            return make_response_json(400, "密码错误")

    if user.state == -1:
        return make_response_json(400, "您的账号已被冻结")

    # 记住登录状态，同时维护current_user
    login_user(user, True, datetime.timedelta(days=30))

    return url_for('user.index')


@api_blue.route('/login_using_password', methods=['POST'])
def login_using_password():
    user_id = request.form.get('email')
    jui = judge_user_id(user_id)

    if jui[0] != 0:
        return make_response_json(quick_response=jui)
    password = request.form.get('password')
    jp = judge_password(password)
    if jp[0] != 0:
        return make_response_json(quick_response=jp)
    return _login(user_id, password)


@api_blue.route('/register_or_login_using_verification_code', methods=['POST'])
def register_or_login_using_verification_code():
    user_id = request.form.get('email')
    password = request.form.get('password')
    if len(password) != 0:
        jp = judge_password(password)
        if jp[0] != 0:
            return make_response_json(quick_response=jp)

    code = request.form.get('code')
    jc = judge_code(user_id, code)
    if jc[0] != 0:
        return make_response_json(quick_response=jc)
    user_exist = True
    try:
        tep = User.get(User.email == user_id)
    except:
        user_exist = False
    if password != "":
        if not user_exist:
            xuehao = user_id.split('@')[0]
            User.create(id=int(xuehao),
                        username=xuehao,
                        password_hash=generate_password_hash(password),
                        email=user_id)
            return make_response_json(200, "注册成功")
        else:
            tep.password_hash = generate_password_hash(password)
            tep.save()
            return make_response_json(200, "密码修改成功")
    else:
        if user_exist:
            return _login(user_id)
        else:
            return make_response_json(401, "请输入密码以完成注册")


def GetUserDict(i) -> dict:
    user = {}
    user['id'] = i.id
    user['username'] = i.username
    user['email'] = i.email
    user['state'] = i.state
    user['score'] = i.score
    user['telephone'] = i.telephone
    user['wechat'] = i.wechat
    user['qq_number'] = i.qq_number
    user['campus_branch'] = i.campus_branch
    user['dormitory'] = i.dormitory
    user['gender'] = i.gender
    user['name_is_published'] = i.name_is_published
    if i.name_is_published == True:
        user['name'] = i.name
    else:
        user['name'] = '保密'
    user['major_is_published'] = i.major_is_published
    if i.major_is_published == True:
        user['major'] = i.major
    else:
        user['major'] = '保密'
    return user


#管理员获取所有用户信息
@api_blue.route('/get_all_user', methods=['GET'])
def get_all_user():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    if current_user.state < User_state.Admin.value:
        return make_response_json(401, "权限不足")

    users = User.select().where(User.state != User_state.Admin.value)
    data_list = []
    for i in users:
        user_dic = GetUserDict(i)
        data_list.append(user_dic)

    if len(data_list) == 0:
        return make_response_json(404, "无用户信息")
    return make_response_json(200, "所有用户信息获取成功", data_list)


#管理员封号
@api_blue.route('/ban_user', methods=['PUT'])
def ban_user():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    if current_user.state < User_state.Admin.value:
        return make_response_json(401, "权限不足")

    #在APIFOX测试运行时current_user未经认证，需要先在apifox上登录后才current_user才有效
    user_id = request.form.get("user_id")
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        tep.state = -1
        tep.save()
        return make_response_json(200, "操作成功")

        #query=User.update(state=-1).where(User.id==user_id)
        #query.execute()


@api_blue.route('/get_user_info', methods=['POST'])
def get_user_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "该用户未通过验证")

    user_id = request.form.get("user_id")
    try:
        tep = User.get(User.id == user_id)
    except:
        return make_response_json(404, "未找到用户")
    else:
        return make_response_json(200, "获取用户数据成功", GetUserDict(tep))


@api_blue.route('/get_item_info', methods=['GET'])
def get_item_info():
    item_id = request.args.get('item_id')
    res = copy.deepcopy(default_res)
    try:
        it = Item.get(Item.id == item_id)
    except Exception as e:
        return make_response_json(404, "未找到此商品")
    else:
        res['statusCode'] = 200
        res['success'] = True
        res['message'] = "已找到商品信息"
        dic = it.__data__
        print(dic)
        dic.pop('id')
        dic.pop('locked_num')
        res['data'] = dic
        dic['publish_time'] = str(dic['publish_time'])
        dic['price'] = float(dic['price'])
        if not current_user.is_authenticated:
            isAdmin = False
            isPub = False
        else:
            isAdmin = (current_user.state == User_state.Admin.value)
            isPub = (it.user_id.id == current_user.id)
        res["isAdmin"] = isAdmin
        res["isPub"] = isPub
    return make_response(jsonify(res))


@api_blue.route('/search', methods=['POST'])
def get_search():
    search_type = request.form.get("search_type")
    if search_type != Item_type.Goods.value and search_type != Item_type.Want.value:
        return make_response_json(400, "搜索类型仅能指定商品或悬赏")

    key_word = request.form.get("key_word")
    order_type = request.form.get("order_type")
    data = []

    #get_data = Item.select().where().exectue()
    if order_type == "time":
        orderWay = (Item.publish_time.desc(), )
    elif order_type == "price":
        orderWay = (Item.price.asc(), )
    else:
        orderWay = (Item.publish_time.desc(), )  # 改：默认其实为相似度

    need = (Item.id, Item.name, Item.user_id, Item.publish_time, Item.price)
    select_need = [Item.name.contains(key_word), Item.type == search_type]
    try:
        start_time = request.form.get("start_time")
        if start_time != "" and start_time is not None:
            start_time = datetime.strptime(start_time, "%Y-%m-%d")
            select_need.append(Item.publish_time >= start_time)
        end_time = request.form.get("end_time")
        if end_time != "" and end_time is not None:
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
            select_need.append(Item.publish_time <= end_time)
    except Exception as e:
        print(e)
        return make_response_json(400, '时间格式错误,应为年-月-日格式')
    else:
        get_data = Item.select(*need).where(*select_need).order_by(
            *orderWay).execute()
        for i in get_data:
            j = i.__data__
            j['price'] = float(j['price'])
            j['publish_time'] = str(j['publish_time'])
            data.append(j)
        return make_response_json(200, "搜索结果如下", data)


@api_blue.route("/change_item_status", methods=["PUT"])
def change_item_status():
    if not current_user.is_authenticated:
        return make_response_json(400, "当前用户未登录")
    data = json.loads(request.get_json())
    try:
        item = Item.get(Item.id == data["item_id"])
    except Exception as e:
        return make_response_json(404, "此商品不存在")
    else:
        if item.type == data["state"]:
            return make_response_json(400, "商品当前状态和希望更改的状态相同")
        else:
            if current_user.state == User_state.Admin.value:
                return make_response_json(200, "操作成功")
            elif current_user.state == User_state.Under_ban.value:
                return make_response_json(400, "您当前已被封号,请联系管理员解封")
            else:
                if current_user.id != item.user_id_id:
                    return make_response_json(400, "不可改变其他人的商品状态")
                else:
                    if data["state"] == Item_state.Freeze.value:
                        return make_response_json(400, "权限不足")
                    else:
                        return make_response_json(200, "操作成功")
