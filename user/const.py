from enum import Enum, unique

#添加 unique 装饰器
@unique
class User_state(Enum):
    #用户状态：0为普通用户，-1为封号，1为管理员
    Normal = 0
    Admin = 1
    Under_ban = -1
    
    # -1 封号
    # 0 游客
    # 1 普通用户
    # 20 管理员
    # 999 系统管理员
    


@unique
class User_Campus_state(Enum):
    SiPing = "四平路校区"
    JiaDing = "嘉定校区"
    HuXi = "沪西校区"
    HuBei = "沪北校区"

@unique
class Gender(Enum):
    Male='男'
    Female='女'
    Undisclosed='保密'

STATE_CHECK='state >='+str(User_state.Under_ban.value)
GENDER_CHECK="gender in ('" + Gender.Male.value + "', '" +Gender.Female.value + "','"+Gender.Undisclosed.value+"')"
CAMPUS_BRANCH_CHECK="campus_branch in ('"+User_Campus_state.SiPing.value +"','"+User_Campus_state.JiaDing.value+"','"+User_Campus_state.HuXi.value+"','"+User_Campus_state.HuBei.value+"')"

