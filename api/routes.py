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
    pattern = re.compile(r'^\d{5,7}@tongji\.edu\.cn$')
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

    return make_response_json(data={"url": url_for('user.index')})


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
                        user_no=xuehao,
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
