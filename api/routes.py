#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue

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
config = os.path.join(curpath, 'verify_code.json')  # [{"time": int(time.time()), "user_id":str, "code":str}]
if not os.path.exists(config):
    with open(config, "w", encoding="utf-8") as fp:
        print("[]", file=fp)


def save_verify_code(code: json):
    with open(config, "w", encoding="utf-8") as fp:
        json.dump(code, fp, indent=4, ensure_ascii=False)


def get_verify_code() -> List[dict]:
    with open(config, "r", encoding="utf-8") as fp:
        return (json.load(fp))


def judge_code_frequency(user_id: str) -> list:
    '''
    验证上次发送验证码间隔是否>1min
    :return [statusCode:0|400, message:str]
    '''
    jui = judge_user_id(user_id)
    if jui[0] != 0:
        return jui
    code_list = get_verify_code()
    save_verify_code(list(filter(lambda x: x["time"] - time < 900, code_list)))  # 验证码有效期15min
    nowtime = int(time.time())
    for code_record in code_list:
        if code_record["user_id"] == user_id:
            if nowtime - code_record["time"] < 59:
                return [400, "验证码申请过于频繁"]
    return [0, ""]


def judge_code(user_id: str, code: str = None) -> list:
    '''
    验证验证码是否正确
    :return [statusCode:0|400, message:str]
    '''
    try:
        code = str(code).strip()
    except:
        return [400, "验证码格式错误"]
    if len(code) == 0:
        return [400, "验证码不可为空"]

    jui = judge_user_id(user_id)
    if jui[0] != 0:
        return jui
    code_list = get_verify_code()
    save_verify_code(list(filter(lambda x: x["time"] - time < 900, code_list)))  # 验证码有效期15min
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
    res = copy.deepcopy(default_res)  # {'success': True, 'statusCode': 200, 'message': '', 'data': {}}
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        jcf = judge_code_frequency(user_id)
        if jcf[0] != 0:
            return make_response(jsonify(jcf))
        verification_code = create_string_number(6)
        ret = send_email("同济跳蚤市场 注册验证码", [user_id], f'您的注册验证码为：{verification_code}。有效期为15分钟。\n此邮件为系统自动发出，请勿回复。')

        code_list = get_verify_code()
        code_list.append({"time": int(time.time()), "user_id": user_id, "code": verification_code.upper()})
        save_verify_code(code_list)
        if ret["status"] == False:
            return make_response_json(400, "验证码邮件发送失败，请重试或联系网站管理员。")
        retcode = 200
        try:
            User.get(User.id == user_id)
        except:
            retcode = 201
        return make_response_json(retcode, "验证码发送成功")


@api_blue.route('/login_using_password', methods=['POST'])
def login_using_password():
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    remember_me = True
    try:
        user = User.get(User.id == user_id)  # 查，此处还可以添加判断用户是否时管理员
    except:
        return make_response_json(400, "账号不存在")
    else:
        # 查到了，判断密码
        if not user.check_password(password):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            return make_response_json(400, "密码错误")
        if user.state == -1:
            return make_response_json(400, "您的账号已被冻结")
        # 记住登录状态，同时维护current_user
        login_user(user, True, datetime.timedelta(days=30))
        return redirect(url_for('user.index'))


@api_blue.route('/register_or_login_using_verification_code', methods=['POST'])
def register_or_login_using_verification_code():
    return


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
    res = copy.deepcopy(default_res)
    data_list = []
    # 判断当前用户是否验证
    if not current_user.is_authenticated:
        res['message'] = "该用户未通过验证"
        res['statusCode'] = 401
        res['success'] = False
    elif current_user.state == User_state.Admin.value:  #如果当前用户是管理员
        users = User.select().where(User.state != User_state.Admin.value)
        for i in users:
            user_dic = GetUserDict(i)
            data_list.append(user_dic)
        res['data'] = data_list

        if len(data_list) > 0:
            res['message'] = "所有用户信息获取成功"
        else:
            res['message'] = "未找到对应用户信息"
            res['statusCode'] = 404
            res['success'] = False

    else:  #非管理员
        res['message'] = "非管理员无此权限"
        res['statusCode'] = 401
        res['success'] = False

    return make_response(jsonify(res))


#管理员封号
@api_blue.route('/ban_user', methods=['PUT'])
def ban_user():
    if request.method == 'PUT':
        res = copy.deepcopy(default_res)
        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        #在APIFOX测试运行时current_user未经认证，需要先在apifox上登录后才current_user才有效
        elif current_user.state == User_state.Admin.value:  #如果当前用户是管理员
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['message'] = "已将对应用户封号"
                tep.state = -1
                tep.save()
                #query=User.update(state=-1).where(User.id==user_id)
                #query.execute()
        else:  #非管理员
            res['message'] = "非管理员无此权限"
            res['statusCode'] = 401
            res['success'] = False

        return make_response(jsonify(res))


@api_blue.route('/get_user_info', methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        res = copy.deepcopy(default_res)

        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        else:
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['data'] = GetUserDict(tep)
                res['message'] = "获取用户数据成功"
        return make_response(jsonify(res))


"""
@api_blue.route('/getlatestorder', methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        res = copy.deepcopy(default_res)

        # 判断当前用户是否验证
        if not current_user.is_authenticated:
            res['message'] = "该用户未通过验证"
            res['statusCode'] = 401
            res['success'] = False
        else:
            user_id = request.form.get("user_id")
            try:
                tep = User.get(User.id == user_id)
            except:
                res['message'] = "未找到对应用户信息"
                res['statusCode'] = 404
                res['success'] = False
            else:
                res['data'] = GetUserDict(tep)
                res['message'] = "获取用户数据成功"
        return make_response(jsonify(res))
"""
<<<<<<< HEAD
@api_blue.route('/get_item_info',methods=['GET'])
def get_item_info():
=======


@api_blue.route('/get_goods_info', methods=['GET'])
def get_goods_data():
>>>>>>> c5c64a4eefda97184741eed44a439eab52cb2b28
    item_id = request.args.get('id')
    need_type = request.args.get("type")
    print(item_id)
    if need_type == "goods":
        bases = Goods
    elif need_type == "want":
        bases = Want
    else:
        bases = None
    res = copy.deepcopy(default_res)
    try:
<<<<<<< HEAD
        it = bases.get(bases.id==item_id)
=======
        it = Goods.get(Goods.id == item_id)
>>>>>>> c5c64a4eefda97184741eed44a439eab52cb2b28
    except Exception as e:
        it = None
    if it is None:
        #报错
        res['statusCode'] = 404
        res['success'] = False
        res['message'] = "未找到商品信息"
        res['data'] = dict()
    else:
        res['statusCode'] = 200
        res['success'] = True
        res['message'] = "已找到商品信息"
        dic = it.__data__
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
            isPub = (it.publisher_id.id == current_user.id)
        res["isAdmin"] = isAdmin
        res["isPub"] = isPub
    return make_response(jsonify(res))

<<<<<<< HEAD
@api_blue.route('/search',methods = ['POST'])
=======

@api_blue.route('/get_want_info', methods=['GET'])
def get_want_data():
    item_id = int(request.args.get("id"))
    res = copy.deepcopy(default_res)
    try:
        it = Want.get(Want.id == item_id)
    except Exception as e:
        it = None
    if it is None:
        #报错
        res['statusCode'] = 404
        res['success'] = False
        res['message'] = "未找到悬赏信息"
        res['data'] = dict()
    else:
        res['statusCode'] = 200
        res['success'] = True
        res['message'] = "已找到悬赏信息"
        dic = it.__data__
        dic.pop('id')
        dic.pop('locked_num')
        dic['publish_time'] = str(dic['publish_time'])
        dic['price'] = float(dic['price'])
        res['data'] = dic
        if not current_user.is_authenticated:
            isAdmin = False
            isPub = False
        else:
            isAdmin = (current_user.state == User_state.Admin.value)
            isPub = it.publisher_id.id == current_user.id
        res["isAdmin"] = isAdmin
        res["isPub"] = isPub
    return make_response(jsonify(res))


@api_blue.route('/search', methods=['POST'])
>>>>>>> c5c64a4eefda97184741eed44a439eab52cb2b28
def get_search():
    search_type = request.form.get("search_type")
    res = copy.deepcopy(default_res)
    res['data'] = list()
    if search_type == "goods" or search_type == 'all':
        search_goods = True
    else:
        search_goods = False
    if search_type == "want" or search_type == 'all':
        search_want = True
    else:
        search_want = False
    if not search_goods and not search_want:
        res['statusCode'] = 400
        res['message'] = "搜索类型仅能指定商品或悬赏"
        res['success'] = False
    else:

        #get_data = bases.select().where().exectue()
        res['statusCode'] = 200
        res['message'] = "已搜索如下结果"
        res['success'] = True
        if search_goods:
            goods_need = (Goods.name, Goods.publisher_id, Goods.publish_time, Goods.price)
            get_data = Goods.select(*goods_need).execute()
            for i in get_data:
                j = i.__data__
                j['price'] = float(j['price'])
                j['type'] = "goods"
                res['data'].append(j)
        if search_want:
            Want_need = Want.name, Want.publisher_id, Want.publish_time, Want.price
            get_data = Want.select(*Want_need).execute()
            for i in get_data:
                j = i.__data__
                j['price'] = float(j['price'])
                j['type'] = "want"
                res['data'].append(j)
        #order

        for i in res['data']:
            i['publish_time'] = str(i['publish_time'])
    return make_response(jsonify(res))
