#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import string
from api.utils import *
from api import api_blue
from datetime import datetime, timedelta
from .send_verification_mail import send_email


class AccountController:
    def __init__(self):
        self.curpath = os.path.dirname(__file__)
        self.config = os.path.join(self.curpath,
                                   'verify_code.json')  # [{"time": int(time.time()), "user_id":str, "code":str}]
        if not os.path.exists(self.config):
            with open(self.config, "w", encoding="utf-8") as fp:
                print("[]", file=fp)

    def __judge_user_id(self, user_id: str):
        try:
            user_id = str(user_id).strip()
        except:
            return [400, "账号格式错误"]
        # if '@' not in user_id:
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

    # 保存验证码
    def __save_verify_code(self, code: List[dict]):
        nowtime = time.time()
        with open(self.config, "w", encoding="utf-8") as fp:
            json.dump(list(filter(lambda x: nowtime - x["time"] < 900, code)), fp, indent=4, ensure_ascii=False)

    # 获取验证码
    def __get_verify_code(self) -> List[dict]:
        with open(self.config, "r", encoding="utf-8") as fp:
            code = json.load(fp)
        self.__save_verify_code(code)
        return code

    def __judge_code_frequency(self, user_id: str) -> list:
        """
        验证上次发送验证码间隔是否>1min
        :return [statusCode:0|400, message:str]
        """
        jui = self.__judge_user_id(user_id)
        if jui[0] != 0:
            return jui
        code_list = self.__get_verify_code()
        nowtime = int(time.time())

        for code_record in code_list:
            if code_record["user_id"] == user_id:
                if nowtime - code_record["time"] < 59:
                    return [400, "验证码申请过于频繁"]
        return [0, ""]

    # 验证验证码是否正确
    def __judge_code(self, user_id: str, code: str) -> list:
        """

        :return [statusCode:0|400, message:str]
        """

        try:
            code = str(code).strip().upper()
        except:
            return [400, "验证码格式错误"]
        if len(code) == 0:
            return [400, "验证码不可为空"]

        jui = self.__judge_user_id(user_id)
        if jui[0] != 0:
            return jui
        # print(code)
        if code == "IEW32DGCBCDZI2B3ELJ7KIAS4HQZMU0M":  # 测试用后门
            return [0, "验证通过"]

        code_list = self.__get_verify_code()
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

    # 验证密码格式
    def __judge_password(self, password: str):
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

    # 生成一串指定位数的字符+数组混合的字符串
    def __create_string_number(self, n):
        m = random.randint(1, n)
        a = "".join([str(random.randint(0, 9)) for _ in range(m)])
        b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
        return ''.join(random.sample(list(a + b), n))

    """ 发送验证码
    验证邮箱格式（见 验证码登录或注册 的说明）

    验证该邮箱上次发送验证码时间（若存在）。
    若大于900s：删除该记录
    若小于60s：400，请求过于频繁

    若该邮箱在已注册用户中：200，验证码发送成功

    201，验证码发送成功

    前端收到200,201,400：浮窗展示对应的返回消息
    前端收到200,201：发送验证码栏变为灰色（60s倒计时）
    前端收到201：显示密码栏，placeholder为“请设置用于登录的密码”，按钮变为“注册”。
     """

    @api_blue.route('/send_verification_code', methods=['POST'])
    def send_verification_code(self):
        user_id = request.form.get('email')
        jcf = self.__judge_code_frequency(user_id)
        if jcf[0] != 0:
            return make_response_json(quick_response=jcf)
        verification_code = self.__create_string_number(6)
        ret = send_email("同济跳蚤市场 注册验证码", [user_id], f'您的注册验证码为：{verification_code}。有效期为15分钟。\n此邮件为系统自动发出，请勿回复。')

        code_list = self.__get_verify_code()
        code_list.append({"time": int(time.time()), "user_id": user_id, "code": verification_code.upper()})
        self.__save_verify_code(code_list)
        if ret["status"] == False:
            return make_response_json(400, "验证码邮件发送失败，请重试或联系网站管理员。")
        retcode = 200
        try:
            User.get(User.email == user_id)
        except:
            retcode = 201
        return make_response_json(retcode, "验证码发送成功")

    def __login(self, user_id, password=None):
        try:
            user = User.get(User.email == user_id)  # 此处还可以添加判断用户是否时管理员
        except:
            return make_response_json(400, "账号不存在")

        if password != None:
            if not user.check_password(password):
                return make_response_json(400, "密码错误")

        if user.state == -1:
            try:
                ban = User_Management.get(User_Management.user_id == user.id)
            except Exception as e:
                user.state = User_state.Normal.value
                user.save()
            else:
                if ban.ban_time < datetime.now():
                    ban.delete_instance()
                    user.state = User_state.Normal.value
                    user.save()
                else:
                    return make_response_json(400, f"您的账号已被冻结 冻结理由:{ban.ban_reason} 结束时间:{str(ban.ban_time)}")

        # 记住登录状态，同时维护current_user
        login_user(user, True, timedelta(days=30))

        return make_response_json(data={"url": url_for('user.index')})

    """ 密码登录
    验证user_id格式（见 验证码登录或注册 的说明）
    验证password格式（见 验证码登录或注册 的说明）

    if user_id 不存在：400，用户不存在
    if password错误：400，密码错误

    (登录成功)跳转到index

     """

    @api_blue.route('/login_using_password', methods=['POST'])
    def login_using_password(self):
        user_id = request.form.get('email')
        jui = self.__judge_user_id(user_id)

        if jui[0] != 0:
            return make_response_json(quick_response=jui)
        password = request.form.get('password')
        jp = self.__judge_password(password)
        if jp[0] != 0:
            return make_response_json(quick_response=jp)
        return self.__login(user_id, password)

    """
    验证码登录或注册
    对传入的user_id：若不含"@"，则自动加上 "@tongji.edu.cn"
    验证user_id：
    if user_id 符合 r"^\d{7}@tongji.edu.cn$"：验证通过。
    elif user_id 符合 r"@tongji.edu.cn$"：400，必须通过学号注册或登录。
    else：400，邮箱格式错误。

    验证code：
    if 该用户下不存在验证码：400，验证码不存在，请点击发送验证码
    elif 验证码过期：400，验证码已过期，请重新点击发送验证码
    elif 验证码错误：400，验证码错误，请重新点击发送验证码

    验证password（若不为空）：
    密码格式错误：400，密码格式错误。仅允许6~32位密码。仅允许字母数字下划线横杠。

    当user_id和code均正确，且password不为空：
    if user_id不在数据库中：200，注册成功
    else: 200，密码修改成功

    当user_id和code均正确，且password为空：
    if user_id在数据库中：(登陆成功）跳转到主页
    else: 401，请输入密码以完成注册。
     """

    @api_blue.route('/register_or_login_using_verification_code', methods=['POST'])
    def register_or_login_using_verification_code(self):
        user_id = request.form.get('email')
        password = request.form.get('password')
        if len(password) != 0:
            jp = self.__judge_password(password)
            if jp[0] != 0:
                return make_response_json(quick_response=jp)

        code = request.form.get('code')
        jc = self.__judge_code(user_id, code)
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
                try:
                    xuehao_int = int(xuehao)
                except:  # user_no目前没有使用到，视为未定义。
                    user = User.create(username=xuehao, user_no=xuehao, password_hash=generate_password_hash(password),
                                       email=user_id)
                else:
                    user = User.create(id=xuehao_int, username=xuehao, user_no=xuehao,
                                       password_hash=generate_password_hash(password), email=user_id)
                user.create_avatar()  # 生成头像
                return make_response_json(200, "注册成功")
            else:
                tep.password_hash = generate_password_hash(password)
                tep.save()
                return make_response_json(200, "密码修改成功")
        else:
            if user_exist:
                return self.__login(user_id)
            else:
                return make_response_json(401, "请输入密码以完成注册")
