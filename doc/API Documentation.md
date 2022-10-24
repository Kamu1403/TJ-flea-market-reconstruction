---
title: 同济跳蚤市场 v1.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.11"

---

# 同济跳蚤市场

> v1.0.0

# 用户管理

## POST 用户发出反馈

POST /api/report

举报物品时跟上物品的id和名称
物品id:1 物品名称:苹果

> Body 请求参数

```json
{
  "item_id": 0,
  "user_id": 0,
  "reason": "string",
  "kind": 0
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» item_id|body|integer| 否 |none|
|» user_id|body|integer| 否 |none|
|» reason|body|string| 否 |none|
|» kind|body|integer| 是 |none|

#### 枚举值

|属性|值|
|---|---|
|» kind|0|
|» kind|1|
|» kind|2|
|» kind|3|
|» kind|4|
|» kind|5|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

# 用户管理/用户资料相关

## GET 获取某用户信息

GET /api/get_user_info

某用户进入他人主页，获取信息
若该用户是游客，返回401；否则开始查找用户
传入user_id格式错误则返回400
若该用户未注册（传入user_id有误)，返回404
若找到用户信息，返回200

如果是传入的user_id参数是current_user.id，则全盘返回；否则返回可见的部分
例如，major_is_published为False时，后端不返回major项，应不显示在前端
name_is_published等等同理

如果不传入user_id参数，则返回current_user的信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|user_id|query|integer| 否 |none|

> 返回示例

> 成功

```json
{
  "data": {
    "campus_branch": "四平路校区",
    "dormitory": "",
    "email": "3@tongji.edu.cn",
    "gender": "保密",
    "id": 3,
    "major": "保密",
    "major_is_published": false,
    "name": "保密",
    "name_is_published": false,
    "qq_number": 0,
    "score": 100,
    "state": 0,
    "telephone": "",
    "username": "3",
    "wechat": ""
  },
  "message": "获取用户数据成功",
  "statusCode": 200,
  "success": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» data|object|true|none||none|
|»» id|integer|true|none||none|
|»» username|string|true|none||用户名|
|»» email|string|true|none||邮箱|
|»» state|integer|true|none||用户状态|
|»» score|integer|true|none||信誉分|
|»» gender|string|true|none||性别|
|»» user_no_is_published|boolean|true|none||是否公开学号|
|»» user_no|string|false|none||学工号|
|»» telephone_is_published|boolean|true|none||是否公开电话|
|»» telephone|string¦null|false|none||电话|
|»» wechat_is_published|boolean|true|none||是否公开微信|
|»» wechat|string¦null|false|none||微信号|
|»» qq_is_published|boolean|true|none||是否公开qq|
|»» qq_number|string¦null|false|none||QQ号|
|»» campus_is_published|boolean|true|none||是否公开所在校区|
|»» campus_branch|string|false|none||所在校区|
|»» dormitory_is_published|boolean|true|none||是否公开所在宿舍|
|»» dormitory|string¦null|false|none||所在宿舍|
|»» name_is_published|boolean|true|none||是否公开姓名|
|»» name|string¦null|false|none||真实姓名|
|»» major_is_published|boolean|true|none||是否公开专业|
|»» major|string¦null|false|none||专业名|
|» message|string|true|none||none|
|» statusCode|integer|true|none||none|
|» success|boolean|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|state|0|
|state|1|
|state|-1|
|gender|男|
|gender|女|
|gender|保密|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

## GET 获取current_user的id

GET /api/get_user_id

401 用户未登录
200 操作成功

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_id|integer|true|none||用户id|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取被封禁用户的信息

GET /api/get_ban_data

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|user_id|query|integer| 否 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» ban_time|string|true|none||none|
|»» ban_reason|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取某用户昵称

GET /api/get_user_username

某用户获取其他用户姓名
查找用户
传入user_id格式错误则返回400
若该用户未注册（传入user_id有误)，返回404
若找到用户信息，返回200

仅返回用户姓名

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|user_id|query|integer| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» name|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## PUT 用户个人信息更改

PUT /api/change_user_info

个人中心页面，完成用户个人信息更改

此操作需前置登录操作
不允许修改邮箱、学号。
后端逻辑：
401：message="未授权“ (未登录,或current user不是本人或管理员)

400：message="请求格式不对"（与他人重复的qq 微信 电话）

404：message="没有找到此用户"
当修改状态成功：200，message="操作成功"

前端逻辑：
4xx：弹出alert框，显示返回的message信息。
200：弹出alert框，随后刷新页面

> Body 请求参数

```json
{
  "username": "string",
  "gender": "男",
  "user_no_is_published": false,
  "telephone_is_published": false,
  "telephone": "string",
  "wechat_is_published": false,
  "wechat": "string",
  "qq_is_published": false,
  "qq_number": 0,
  "campus_is_published": false,
  "campus_branch": "四平路校区",
  "dormitory_is_published": false,
  "dormitory": "友园7号楼",
  "name_is_published": false,
  "name": "string",
  "major_is_published": false,
  "major": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» username|body|string| 是 |用户名|
|» gender|body|string| 是 |性别|
|» user_no_is_published|body|boolean| 是 |是否公开学号|
|» telephone_is_published|body|boolean| 是 |是否公开电话|
|» telephone|body|string¦null| 是 |电话|
|» wechat_is_published|body|boolean| 是 |是否公开微信|
|» wechat|body|string¦null| 是 |微信号|
|» qq_is_published|body|boolean| 是 |是否公开qq|
|» qq_number|body|integer¦null| 是 |QQ号|
|» campus_is_published|body|boolean| 是 |是否公开所在校区|
|» campus_branch|body|string| 是 |所在校区|
|» dormitory_is_published|body|boolean| 是 |是否公开所在宿舍|
|» dormitory|body|string¦null| 是 |所在宿舍|
|» name_is_published|body|boolean| 是 |是否公开姓名|
|» name|body|string¦null| 是 |真实姓名|
|» major_is_published|body|boolean| 是 |是否公开专业|
|» major|body|string¦null| 是 |专业名|

#### 枚举值

|属性|值|
|---|---|
|» gender|男|
|» gender|女|
|» gender|保密|
|» campus_branch|四平路校区|
|» campus_branch|嘉定校区|
|» campus_branch|沪西校区|
|» campus_branch|沪北校区|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 用户管理/管理员操作

## GET 管理员获取所有反馈

GET /api/get_reports

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» unread|[integer]|true|none||none|
|»» read|[integer]|true|none||none|
|»» replied|[integer]|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 管理员查看所有用户

GET /api/get_all_user

401 非管理员
200 操作成功

> 返回示例

> 成功

```json
{
  "data": [
    {
      "id": 4607403,
      "username": "田洋",
      "email": "p.vpmwmrxr@oxpwmf.ws",
      "state": 1,
      "score": 68,
      "campus_branch": "沪西校区",
      "gender": "保密",
      "name_is_published": true,
      "major_is_published": true,
      "wechat": null,
      "major": "计算机科学与技术",
      "telephone": "18192318118",
      "name": "叶超",
      "dormitory": null,
      "qq_number": 96717755
    }
  ],
  "message": "所有用户信息获取成功",
  "statusCode": 200,
  "success": true
}
```

```json
{
  "data": [
    {
      "id": 9004441,
      "username": "龙丽",
      "email": "f.fdmpb@bomukeyph.中国",
      "state": -1,
      "score": -24,
      "campus_branch": "四平路校区",
      "gender": "保密",
      "name_is_published": true,
      "major_is_published": false,
      "name": "叶秀兰",
      "telephone": "18128870865",
      "dormitory": null,
      "major": "软件工程",
      "qq_number": null,
      "wechat": "adipisicing"
    }
  ],
  "message": "所有用户信息获取成功",
  "statusCode": 200,
  "success": true
}
```

```json
{
  "data": [
    {
      "campus_branch": "四平路校区",
      "dormitory": "",
      "email": "123@tongji.edu.cn",
      "gender": "保密",
      "id": 123,
      "major": "保密",
      "major_is_published": false,
      "name": "保密",
      "name_is_published": false,
      "qq_number": 0,
      "score": 100,
      "state": -1,
      "telephone": "",
      "username": "123",
      "wechat": ""
    },
    {
      "campus_branch": "四平路校区",
      "dormitory": "",
      "email": "321@tongji.edu.cn",
      "gender": "保密",
      "id": 321,
      "major": "保密",
      "major_is_published": false,
      "name": "保密",
      "name_is_published": false,
      "qq_number": 0,
      "score": 100,
      "state": 0,
      "telephone": "",
      "username": "321",
      "wechat": ""
    },
    {
      "campus_branch": "四平路校区",
      "dormitory": "",
      "email": "1951705@tongji.edu.cn",
      "gender": "保密",
      "id": 1951705,
      "major": "保密",
      "major_is_published": false,
      "name": "保密",
      "name_is_published": false,
      "qq_number": 0,
      "score": 100,
      "state": -1,
      "telephone": "",
      "username": "1951705",
      "wechat": ""
    }
  ],
  "message": "所有用户信息获取成功",
  "statusCode": 200,
  "success": true
}
```

```json
{
  "data": [
    {
      "id": 4607403,
      "username": "田洋",
      "email": "p.vpmwmrxr@oxpwmf.ws",
      "state": 1,
      "score": 68,
      "campus_branch": "沪西校区",
      "gender": "保密",
      "name_is_published": true,
      "major_is_published": true,
      "wechat": null,
      "major": "",
      "telephone": "18192318118",
      "name": "",
      "dormitory": null,
      "qq_number": 96717755
    }
  ],
  "message": "所有用户信息获取成功",
  "statusCode": 200,
  "success": true
}
```

```json
{
  "data": {},
  "message": "非管理员无此权限",
  "statusCode": 401,
  "success": false
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» username|string|true|none||用户名|
|»» email|string|true|none||邮箱|
|»» state|integer|true|none||用户状态|
|»» score|integer|true|none||信誉分|
|»» gender|string|true|none||性别|
|»» user_no_is_published|boolean|true|none||是否公开学号|
|»» user_no|string|false|none||学工号|
|»» telephone_is_published|boolean|true|none||是否公开电话|
|»» telephone|string¦null|false|none||电话|
|»» wechat_is_published|boolean|true|none||是否公开微信|
|»» wechat|string¦null|false|none||微信号|
|»» qq_is_published|boolean|true|none||是否公开qq|
|»» qq_number|string¦null|false|none||QQ号|
|»» campus_is_published|boolean|true|none||是否公开所在校区|
|»» campus_branch|string|false|none||所在校区|
|»» dormitory_is_published|boolean|true|none||是否公开所在宿舍|
|»» dormitory|string¦null|false|none||所在宿舍|
|»» name_is_published|boolean|true|none||是否公开姓名|
|»» name|string¦null|false|none||真实姓名|
|»» major_is_published|boolean|true|none||是否公开专业|
|»» major|string¦null|false|none||专业名|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|state|0|
|state|1|
|state|-1|
|gender|男|
|gender|女|
|gender|保密|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

## PUT 管理员修改用户状态

PUT /api/change_user_state

401 非管理员
200 成功

### 支持传入的状态：
- "0": "普通用户",
- "1": "管理员",
- "-1": "封号用户"

当且仅当封号时需要有封号截止时间以及封号理由

> Body 请求参数

```json
{
  "user_id": 0,
  "user_state": 0,
  "ban_time": "string",
  "ban_reason": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» user_id|body|integer| 是 |User表主键|
|» user_state|body|integer| 是 |用户状态|
|» ban_time|body|string| 否 |none|
|» ban_reason|body|string| 否 |none|

#### 枚举值

|属性|值|
|---|---|
|» user_state|0|
|» user_state|1|
|» user_state|-1|

> 返回示例

> 成功

```json
{
  "data": {},
  "message": "已将对应用户封号",
  "statusCode": 200,
  "success": true
}
```

```json
{
  "data": {},
  "message": "非管理员无此权限",
  "statusCode": 401,
  "success": false
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## GET 管理员获取所有订单

GET /api/get_all_order

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[object]|true|none||none|
|»» order_id|integer|true|none||none|
|»» item_id_list|[integer]|true|none||none|
|»» user_id|integer|true|none||none|
|»» op_user_id|integer|true|none||none|
|»» state|integer|true|none||none|

## GET 管理员获取单条反馈

GET /api/admin_get_report

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|feedback_id|query|integer| 否 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_id|integer|true|none||none|
|»» publish_time|string|true|none||none|
|»» kind|integer|true|none||none|
|»» state|integer|true|none||none|
|»» feedback_content|string|true|none||none|
|»» reply_content|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|kind|0|
|kind|1|
|kind|2|
|kind|3|
|kind|4|
|kind|5|
|state|0|
|state|1|
|state|-1|

## POST 管理员回复反馈

POST /api/reply_feedback

> Body 请求参数

```json
{
  "id": 0,
  "reply_content": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» id|body|integer| 是 |none|
|» reply_content|body|string| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 订单管理

## POST 订单评价

POST /api/order_evaluate

对于已经完成的订单，在确认完成后，已完成订单会显示一个订单评价按钮，点击跳转到填写评价界面。

用户在该页面填写评价并提交
后端：
200：评价提交成功   message="评价提交成功"
401：未授权（未登录)  message=
400：请求格式不对（id不合理，只有已完成订单才可评价）
404：不存在的订单（id是整数但是不在数据库）

前端：
4xx:alert弹窗输出message
200: 跳转到订单管理页面

评价是不是还需要删除，修改追评之类的

> Body 请求参数

```json
{
  "order_id": 0,
  "feedback_content": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» order_id|body|integer| 是 |none|
|» feedback_content|body|string| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» url|string|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取用户最近所有订单（用state区分）

GET /api/get_order

获取当前登录用户最近range天的订单（订单双方均要考虑）
range不指定则为全时段

返回参数：订单id列表(即data是一个array，里面全是订单的id)

statusCode
#200 
正常返回，等待对方确认和自己确认订单均正常显示
message:"返回订单"
data是一个列表，里面存储着所有需要的信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|range|query|integer| 否 |none|

> 返回示例

> 成功

```json
null
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» data|[object]|true|none||none|
|»» order_id|integer|true|none||none|
|»» item_id_list|[integer]|true|none||none|
|»» user_id|integer|true|none||none|
|»» op_user_id|integer|true|none||none|
|»» state|integer|true|none||none|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|

## POST 提交订单

POST /api/order_post

从生成订单页面(/order/generate/item_id/)调用该api

通过此api(/api/get_address)获取当前用户的所有地址信息
若返回404则让用户添加地址信息（弹出一个框添加）
get_address返回200继续：

以下message均以Goods视角：
该返回statusCode
# 201
成功后跳转到/order/manage 页面
message="订单生成成功，请等待商家确认"
(也可做一个中间页面，要么跳manage页面，要么跳原商品页面）
此时data返回url

# 400
请求格式不对
比如没有选定自己的联系地址（此时前端最好应该阻止提交）
通过发包等操作使得num,item_id,contact_id非法也返回400

约定一个订单的所有物品都应该属于一个商家，否则应该拆分成多个订单
或者 列表中item_id所对应的发布者不是同一个人，此时也返回400
（即，我们不允许不同的商家的物品集合出现在一个订单中）
message="请求格式不对"

# 404
A下单后，B接着下单了，此时库存已清空
而A的订单还未得到双方确认
此时message="您想要的商品正被锁定，可添加至收藏或与商家联系"

# 

> Body 请求参数

```json
{
  "item_info": [
    {
      "item_id": 0,
      "num": 0
    }
  ],
  "contact_id": 0,
  "note": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» item_info|body|[object]| 是 |none|
|»» item_id|body|integer| 是 |none|
|»» num|body|integer| 是 |none|
|» contact_id|body|integer| 是 |none|
|» note|body|string| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object¦null|true|none||none|
|»» order_id|integer|true|none||返回manage的url|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取review内容

GET /api/get_review

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|review_id|query|integer| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_id|integer|true|none||发布者的学号|
|»» publish_time|string|true|none||发布时间|
|»» feedback_content|string¦null|false|none||详细反馈|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 通过订单id获取评价信息

GET /api/get_review_by_order

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|query|integer| 否 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_review_id|integer|true|none||无则为-1|
|»» user_review_content|object|false|none||none|
|»»» id|integer|true|none||ID|
|»»» user_id|integer|true|none||发布者的学号|
|»»» publish_time|string|true|none||发布时间|
|»»» feedback_content|string¦null|false|none||详细反馈|
|»» op_user_review_id|integer|true|none||none|
|»» op_user_review_content|object|false|none||none|
|»»» id|integer|true|none||ID|
|»»» user_id|integer|true|none||发布者的学号|
|»»» publish_time|string|true|none||发布时间|
|»»» feedback_content|string¦null|false|none||详细反馈|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取订单详细信息

GET /api/get_order_info

# 401 
未登录，或登录用户不是管理员或者不是订单双方

# 404 
找不到订单

# 200
返回订单信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|query|integer| 否 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_id|integer|true|none||订单发起者的主键|
|»» payment|number|true|none||总价|
|»» state|integer|true|none||订单状态|
|»» create_time|string|true|none||创建时间|
|»» confirm_time|string¦null|false|none||双方确认时间|
|»» end_time|string¦null|false|none||完成时间|
|»» close_time|string¦null|false|none||关闭时间（被一方取消）|
|»» note|string¦null|false|none||订单备注|
|»» item_info|[object]|true|none||none|
|»»» quantity|integer|true|none||购买数量此项乘对应商品/悬赏的单价，再与订单中其他物品相加等于订单中的总价|
|»»» item_id|integer|true|none||订单对应的物品ID|
|»»» price|number|true|none||生成订单时物品的单价|
|»» campus_branch|string|true|none||none|
|»» telephone|string|true|none||none|
|»» name|string|true|none||none|
|»» full_address|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|state|-1|
|state|0|
|state|1|
|state|2|

## POST 生成订单

POST /api/generate_order

从商品详情页面调用该api

以下message均以Goods视角：

返回statusCode
# 200
成功后跳转到/order/generate/item_id/ 页面
message="跳转到订单生成页面"
此时data返回url

# 400
请求格式不对
message="请求格式不对"

# 401
无权限（游客）
message="请先登录"

# 404
有人下单了但库存已清空
但订单还未得到双方确认
此时message="您想要的商品正被锁定，可添加至收藏或与商家联系"

> Body 请求参数

```json
{
  "item_id": 0
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» item_id|body|integer| 是 |物品id，由该项得发布者（商家）ID|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object¦null|true|none||none|
|»» url|string|false|none||201时跳转至generate页面|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取某订单是否被评价

GET /api/get_user_is_review

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|query|integer| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» is_review|boolean|true|none||none|
|»» op_is_review|boolean|true|none||none|
|»» review_id|integer|false|none||买方|
|»» op_review_id|integer|true|none||卖方|
|»» user_name|string|true|none||none|
|»» op_user_name|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 根据订单获取商品id

GET /api/get_item_id_by_order

根据订单id获取商品id和对应商品的购买数量
从而得到商品信息

如果当前登录的不是订单双方或者管理员，返回401
如果没有找到订单，返回404
否则200

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|query|integer| 是 |none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[object]|true|none||none|
|»» item_id|integer|true|none||none|
|»» quantity|integer|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## PUT 订单状态更改

PUT /api/change_order_state

此操作需前置登录操作

后端逻辑：
当订单的当前状态和希望更改的状态相同：
401：message="未授权“ (未登录,或current user不是订单双方或管理员)
或者current user不是管理员时发生以下情形，也返回401：
1、订单还没确认就想完成订单
2、尝试修改已完成/已关闭的订单状态
3、非悬赏发布者完成悬赏订单，非商品购买者完成商品订单

400：message="请求格式不对"(state出现了三种状态以外的其它状态或要修改的状态与原状态相同）
404：message="没有找到此订单"
当修改状态成功：200，message="操作成功"

前端逻辑：
4xx：弹出alert框，显示返回的message信息。
200：弹出alert框，随后刷新页面

state仅有三种状态：
        {
            "1": "已确认（双方）",
            "2": "已完成",
            "-1": "已关闭"
        }

对于已确认的订单，取消者需要扣除5分信誉分

> Body 请求参数

```json
{
  "order_id": 0,
  "state": -1
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» order_id|body|integer| 是 | 订单id|none|
|» state|body|integer| 是 | 订单状态|-1,已关闭；0,已生成 未确认；1,已确认（双方）；2,已完成|

#### 详细说明

**» state**: -1,已关闭；0,已生成 未确认；1,已确认（双方）；2,已完成
因为发起者默认确认，只需对方确认即可从状态0->1

#### 枚举值

|属性|值|
|---|---|
|» state|-1|
|» state|0|
|» state|1|
|» state|2|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

# 订单管理/地址管理

## POST 用户收货地址添加

POST /api/address

前端支持用户添加地址信息。
添加多个默认地址，则默认指定最后一个添加的为默认地址。
201：添加成功
401：未登录

> Body 请求参数

```json
[
  {
    "default": true,
    "campus_branch": "四平路校区",
    "telephone": "string",
    "name": "string",
    "full_address": "string"
  }
]
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|array[object]| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|操作成功或失败|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## PUT 用户收货地址修改

PUT /api/address

前端支持用户添加地址信息。
添加多个默认地址，则默认指定最后一个添加的为默认地址。
200：操作成功
401：未登录

> Body 请求参数

```json
[
  {
    "id": 0,
    "default": true,
    "campus_branch": "四平路校区",
    "telephone": "string",
    "name": "string",
    "full_address": "string"
  }
]
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|array[object]| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|操作成功或失败|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## DELETE 用户收货地址删除

DELETE /api/address

指定contact_id 删除对应联系地址
删除默认地址，则随机指定一个地址为默认地址，除非没有地址了
200：操作成功
401：未登录

> Body 请求参数

```json
[
  {
    "contact_id": 0
  }
]
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|array[object]| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|操作成功或失败|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## GET 获取当前用户的所有地址信息

GET /api/get_address

获取当前登录用户的所有地址信息

# 200
message="获取成功“

# 404
未设置任何联系地址

# 401
当前用户未登录

# 

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[[Address](#schemaaddress)]¦null|true|none||none|
|»» id|integer|true|none||自增主键|
|»» default|boolean|false|none|是否为默认收货地址|none|
|»» campus_branch|string|true|none||所在校区|
|»» telephone|string|true|none|手机号|none|
|»» name|string|true|none|收货人姓名|none|
|»» full_address|string|true|none|详细地址|none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

# 用户状态更改

## POST 密码登录

POST /api/login_using_password

验证user_id格式（见 验证码登录或注册 的说明）
验证password格式（见 验证码登录或注册 的说明）

if user_id 不存在：400，用户不存在
if password错误：400，密码错误

(登录成功)跳转到index

> Body 请求参数

```yaml
email: 1951705@tongji.edu.cn
password: "1951705"

```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» email|body|string| 是 ||none|
|» password|body|string| 是 ||none|

> 返回示例

> 登录成功

```json
{
  "success": true,
  "statusCode": 200,
  "message": "",
  "data": {
    "url": "/user/index"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|登录成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» url|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## POST 验证码登录或注册

POST /api/register_or_login_using_verification_code

对传入的user_id：若不含"@"，则自动加上 "@tongji.edu.cn"
验证user_id：
if user_id 符合 r"^\d{7}@tongji\.edu\.cn$"：验证通过。
elif user_id 符合 r"@tongji\.edu\.cn$"：400，必须通过学号注册或登录。
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

前端收到200：跳转回登录模块
前端收到400或401：浮窗展示对应的返回消息
前端收到401：展示密码栏，placeholder为“请设置用于登录的密码”，按钮变为“注册”。

> Body 请求参数

```yaml
email: 1951705@tongji.edu.cn
code: 123AbC
password: "1951705"

```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» email|body|string| 是 ||none|
|» code|body|string| 是 ||随机生成的验证码|
|» password|body|string| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## GET 登出

GET /logout

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 发送验证码

POST /api/send_verification_code

验证邮箱格式（见 验证码登录或注册 的说明）

验证该邮箱上次发送验证码时间（若存在）。
若大于900s：删除该记录
若小于60s：400，请求过于频繁

若该邮箱在已注册用户中：200，验证码发送成功

201，验证码发送成功

前端收到200,201,400：浮窗展示对应的返回消息
前端收到200,201：发送验证码栏变为灰色（60s倒计时）
前端收到201：显示密码栏，placeholder为“请设置用于登录的密码”，按钮变为“注册”。

> Body 请求参数

```yaml
email: 1951705@tongji.edu.cn

```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» email|body|string| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

# 物品管理

## PUT 商品数量更改

PUT /api/change_item_num

后端逻辑：
当操作人非商品发起用户：401，不可修改其他人的商品数量
200，操作成功

前端逻辑：
40x：alert
200：alert

> Body 请求参数

```json
{
  "item_id": 0,
  "num": 0
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» item_id|body|integer| 是 ||none|
|» num|body|integer| 是 | 修改之后的个数|none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 主页物品展示

GET /api/item_to_show

首页展示部分物品

请求参数为时间范围(即距今range天内)和最大展示数目(即最多max_num)
两个参数都是若空则选择全部

响应为200，各个物品的详细信息

对于未注册用户也支持，因为适用于主页

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|range|query|integer| 否 ||单位是天|
|max_num|query|integer| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» show|[object]|true|none||none|
|»»» id|integer|true|none||自增ID|
|»»» name|string|true|none||商品名|
|»»» user_id|integer|true|none||发布者的学号|
|»»» publish_time|string|true|none||发布时间|
|»»» price|number|true|none||单价|
|»»» tag|string¦null|true|none||Tag,用于分类|
|»»» type|integer|true|none||none|
|»»» shelved_num|integer|true|none||上架数量|
|»»» description|string¦null|true|none||详细描述|
|»»» state|integer|true|none|商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|type|1|
|type|0|
|state|0|
|state|-1|
|state|1|

## GET 获取物品头图

GET /api/get_item_head_pic

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|item_id|query|integer| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» url|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 用户获取单个物品信息

GET /api/get_item_info

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|item_id|query|integer| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» isPub|boolean|true|none|当前用户是否为上传者|none|
|» isAdmin|boolean|true|none|当前用户是否为管理员|none|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» name|string|true|none||商品名|
|»» user_id|integer|true|none||发布者的学号|
|»» publish_time|string|true|none||发布时间|
|»» price|number|true|none||单价|
|»» tag|string¦null|true|none||Tag,用于分类|
|»» type|integer|true|none||none|
|»» shelved_num|integer|true|none||上架数量|
|»» description|string¦null|true|none||详细描述|
|»» state|integer|true|none|商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|type|1|
|type|0|
|state|0|
|state|-1|
|state|1|

## GET 获取用户所发布的物品

GET /api/get_user_item

获取user_id所发布的物品
若不指定，则获取current_user的

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|user_id|query|integer| 否 ||用户id|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||自增ID|
|»» name|string|true|none||商品名|
|»» user_id|integer|true|none||发布者的学号|
|»» publish_time|string|true|none||发布时间|
|»» price|number|true|none||单价|
|»» tag|string¦null|true|none||Tag,用于分类|
|»» type|integer|true|none||none|
|»» shelved_num|integer|true|none||上架数量|
|»» description|string¦null|true|none||详细描述|
|»» state|integer|true|none|商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|
|type|1|
|type|0|
|state|0|
|state|-1|
|state|1|

## GET 获取物品图片

GET /api/get_item_pics

传入商品id，返回图片url列表。

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|item_id|query|integer| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

*图片url列表*

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object¦null|true|none||none|
|»» url|[string]|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## PUT 修改物品信息

PUT /api/change_item_data

仅有管理员可修改所有人发布的物品信息
单个用户仅能修改自己所发布的物品信息

> Body 请求参数

```json
{
  "id": 0,
  "name": "string",
  "price": 0,
  "tag": "string",
  "shelved_num": 1,
  "description": "string"
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» id|body|integer| 是 ||自增ID|
|» name|body|string| 是 ||商品名|
|» price|body|number| 是 ||单价|
|» tag|body|string¦null| 是 ||Tag,用于分类|
|» shelved_num|body|integer| 是 ||上架数量|
|» description|body|string¦null| 是 ||详细描述|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## PUT 商品状态更改

PUT /api/change_item_state

后端逻辑：
当商品的当前状态和希望更改的状态相同：400，商品当前状态和希望更改的状态相同
当操作人为管理员：200，操作成功
当操作人非商品发起用户：401，不可修改其他人的商品状态
若希望修改item_status为-1：401，权限不足
200，操作成功

前端逻辑：
40x：弹出alert框，显示返回的message信息。
200：弹出alert框，随后刷新页面。

> Body 请求参数

```json
{
  "item_id": 0,
  "state": 0
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» item_id|body|integer| 是 | 商品id|none|
|» state|body|integer| 是 | 商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|» state|0|
|» state|-1|
|» state|1|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## POST 物品搜索

POST /api/search

search_type 悬赏还是商品
order_type 排列方式

> Body 请求参数

```json
{
  "search_type": 0,
  "start_time": "string",
  "end_time": "string",
  "order_type": "time",
  "key_word": "string",
  "tag": "string",
  "range_min": 0,
  "range_max": 0
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» search_type|body|integer| 是 ||none|
|» start_time|body|string| 是 ||none|
|» end_time|body|string| 是 ||none|
|» order_type|body|string| 是 ||none|
|» key_word|body|string| 是 ||none|
|» tag|body|string| 否 | 一定是tag枚举变量中的一个值|none|
|» range_min|body|integer| 否 | 和range_max必须一同出现|none|
|» range_max|body|integer| 否 ||none|

#### 枚举值

|属性|值|
|---|---|
|» search_type|0|
|» search_type|1|
|» order_type|time|
|» order_type|price|
|» order_type|name|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» item_list|object|true|none||none|
|»»» id|integer|true|none||自增ID|
|»»» name|string|true|none||商品名|
|»»» publish_time|string|true|none||发布时间|
|»»» price|number|true|none||单价|
|»» total_count|integer|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 物品管理/收藏历史管理

## GET 获取用户的历史

GET /api/get_history

默认用current_user
401 未登录
200 操作成功

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|range_max|query|integer| 否 ||none|
|range_min|query|integer| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» history_list|object|true|none||none|
|»»» id|integer|true|none||ID|
|»»» item_id|integer|true|none||物品ID|
|»»» visit_time|string|true|none||访问时间|
|»» total_count|integer|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取当前用户是否收藏了某商品

GET /api/get_item_favor

默认用current_user
401 未登录
200 操作成功

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|item_id|query|integer| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|boolean|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## DELETE 删除用户收藏

DELETE /api/delete_favor

直接删current_user的收藏
200 操作成功
404 没找到对应的收藏（剩下的其它找到了的收藏会删除）
401 没登录

> Body 请求参数

```json
{
  "item_id_list": [
    0
  ]
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» item_id_list|body|[integer]| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## DELETE 删除用户历史

DELETE /api/delete_history

直接删current_user的历史
200 操作成功
404 没找到对应的历史（剩下的其它找到了的历史会删除）
401 没登录

> Body 请求参数

```json
{
  "item_id_list": [
    0
  ]
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» item_id_list|body|[integer]| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## POST 收藏物品

POST /api/add_favor

404 不存在对应物品（有一个不存在，所有的物品都不添加）
400 重复添加（重复的那个不添加，其它的正常添加）
201 全部添加成功
401 未登录

> Body 请求参数

```json
{
  "item_id_list": [
    0
  ]
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» item_id_list|body|[integer]| 是 ||要收藏的商品/悬赏id列表|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## GET 获取用户的收藏

GET /api/get_favor

默认用current_user
401 未登录
200 操作成功

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|range_max|query|integer| 否 ||none|
|range_min|query|integer| 否 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||ID|
|»» item_id|integer|true|none||物品ID|
|»» collect_time|string|true|none||收藏时间|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 物品管理/物品发布

## POST 发布物品信息

POST /api/post_item_info

后端逻辑：
try:
生成新物品id，填入传入的信息（除图片MD5）到数据库
根据图片MD5从临时文件夹找到图片，移入物品对应文件夹中
物品相关联的图片urls: [[MD5, 0/1(是否为头图)], [MD5, 0/1], ...]
如果没有1：默认第一张为头图
如果没有图：一张默认图
201, 发布成功
except e:
  400, 发布失败：{repr(e)}
401,未登录，无发布权限

前端逻辑：
201：alert，刷新页面
400：alert，不刷新页面
401：alert，不刷新页面：无发布权限

> Body 请求参数

```json
{
  "name": "想验同间容",
  "price": 35,
  "tag": "in",
  "type": 92,
  "shelved_num": 8,
  "description": "id incididunt sed",
  "url": "http://hlojxqn.st/dtlzgxsy",
  "urls": null
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» name|body|string| 是 ||none|
|» price|body|number| 是 ||none|
|» tag|body|string| 是 ||none|
|» type|body|integer| 是 ||none|
|» shelved_num|body|integer| 是 ||none|
|» description|body|string¦null| 否 ||none|
|» urls|body|[object]¦null| 否 | 其它图片MD5集合|none|
|»» MD5|body|string| 是 ||none|
|»» is_cover_pic|body|boolean| 是 ||none|

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|[标准API接口](#schema%e6%a0%87%e5%87%86api%e6%8e%a5%e5%8f%a3)|

## POST 发布物品图片

POST /api/post_item_pic

传张图片到服务器

后端逻辑：
try:
  服务器成功收到图片：
  将图片放在某个文件夹下，强转成jpg格式，根据其MD5重命名。
  200，图片上传成功，data=str(图片MD5码)。
except e:
  400，e
后期可以考虑加入流量控制，防止恶意堵塞服务器。

前端逻辑：
try:
    200：提示图片上传成功，
    urls加入该MD5码（并展示到页面上）
except:
    alert(上传失败)

> Body 请求参数

```yaml
file: file://C:\Users\ellye\Pictures\视频项目\SAUME8J]${8]2CE(JGDT058.png

```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» file|body|string(binary)| 否 ||none|

> 返回示例

> 成功

```json
{
  "success": true,
  "statusCode": 200,
  "message": "图片上传成功",
  "data": "一行MD5码"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 聊天室管理

## GET 获取最后一条聊天记录

GET /api/get_last_msg

此操作需前置登录操作

获取当前用户的会话列表

后端逻辑：
200 返回 json格式的信息：{ 'user_id': {'last_msg':lastmsg,'sender':sender},...}
401 用户未授权登录

前端逻辑：
4xx:  返回登陆页面
200：无消息即为空，否则在会话框下侧限长显示最后一条消息

> 返回示例

> 成功

```json
{
  "data": {
    "1951566": {
      "last_msg": "你好",
      "sender": 1950084
    }
  },
  "message": "获取最后消息成功",
  "statusCode": 200,
  "success": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» user_id|object|true|none||none|
|»»» sender|integer|true|none||none|
|»»» last_msg|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取会话列表

GET /api/get_meet_list

此操作需前置登录操作

获取当前用户的会话列表

后端逻辑：
200 返回 json
401 用户未授权登录

前端逻辑：
4xx: 返回登陆页面
200：在聊天室左侧显示会话列表

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» meet_list|[string]|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

## GET 获取未读消息条数

GET /api/get_message_cnt

此操作需前置登录操作（应当是所有页面的head都需要获取，可以考虑放在session中）

获取当前用户的所有未读信息条数

后端逻辑：
200 返回count
401 用户未授权登录

前端逻辑：
4xx: 未读消息栏不显示数字
200：count==0时不显示数字，否则在消息图标右上角显示数字气泡

> 返回示例

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» success|boolean|true|none||none|
|» statusCode|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|
|»» unread|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

# 数据模型

<h2 id="tocS_Item">Item</h2>

<a id="schemaitem"></a>
<a id="schema_Item"></a>
<a id="tocSitem"></a>
<a id="tocsitem"></a>

```json
{
  "id": 0,
  "name": "string",
  "user_id": 0,
  "publish_time": "string",
  "price": 0,
  "tag": "string",
  "type": 1,
  "shelved_num": 1,
  "locked_num": 0,
  "description": "string",
  "state": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||自增ID|
|name|string|true|none||商品名|
|user_id|integer|true|none||发布者的学号|
|publish_time|string|true|none||发布时间|
|price|number|true|none||单价|
|tag|string¦null|true|none||Tag,用于分类|
|type|integer|true|none||none|
|shelved_num|integer|true|none||上架数量|
|locked_num|integer|true|none||锁定数量|
|description|string¦null|true|none||详细描述|
|state|integer|true|none|商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|type|1|
|type|0|
|state|0|
|state|-1|
|state|1|

<h2 id="tocS_Contact">Contact</h2>

<a id="schemacontact"></a>
<a id="schema_Contact"></a>
<a id="tocScontact"></a>
<a id="tocscontact"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "default": true,
  "campus_branch": "四平路校区",
  "telephone": "string",
  "name": "string",
  "full_address": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|user_id|integer|true|none||订单发起者学号|
|default|boolean|false|none|是否为默认收货地址|none|
|campus_branch|string|true|none||所在校区|
|telephone|string|true|none|手机号|none|
|name|string|true|none|收货人姓名|none|
|full_address|string|true|none|详细地址|none|

#### 枚举值

|属性|值|
|---|---|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

<h2 id="tocS_Order with item_id">Order with item_id</h2>

<a id="schemaorder with item_id"></a>
<a id="schema_Order with item_id"></a>
<a id="tocSorder with item_id"></a>
<a id="tocsorder with item_id"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "payment": 0,
  "state": -1,
  "create_time": "string",
  "confirm_time": "string",
  "end_time": "string",
  "close_time": "string",
  "note": "string",
  "item_info": [
    {
      "quantity": 0,
      "item_id": 0,
      "price": 0
    }
  ],
  "campus_branch": "string",
  "telephone": "string",
  "name": "string",
  "full_address": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||Order ID|
|user_id|integer|true|none||订单发起者的主键|
|payment|number|true|none||总价|
|state|integer|true|none||订单状态|
|create_time|string|true|none||创建时间|
|confirm_time|string¦null|false|none||双方确认时间|
|end_time|string¦null|false|none||完成时间|
|close_time|string¦null|false|none||关闭时间（被一方取消）|
|note|string¦null|false|none||订单备注|
|item_info|[object]|true|none||none|
|» quantity|integer|true|none||购买数量此项乘对应商品/悬赏的单价，再与订单中其他物品相加等于订单中的总价|
|» item_id|integer|true|none||订单对应的物品ID|
|» price|number|true|none||单价|
|campus_branch|string|true|none||none|
|telephone|string|true|none||none|
|name|string|true|none||none|
|full_address|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|state|-1|
|state|0|
|state|1|
|state|2|

<h2 id="tocS_History">History</h2>

<a id="schemahistory"></a>
<a id="schema_History"></a>
<a id="tocShistory"></a>
<a id="tocshistory"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "item_id": 0,
  "visit_time": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|user_id|integer|true|none||访问者的学号|
|item_id|integer|true|none||物品ID|
|visit_time|string|true|none||访问时间|

<h2 id="tocS_Item_state">Item_state</h2>

<a id="schemaitem_state"></a>
<a id="schema_Item_state"></a>
<a id="tocSitem_state"></a>
<a id="tocsitem_state"></a>

```json
{
  "state": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|state|integer|true|none|商品状态|0正常 -1管理员下架 1自己下架|

#### 枚举值

|属性|值|
|---|---|
|state|0|
|state|-1|
|state|1|

<h2 id="tocS_Address">Address</h2>

<a id="schemaaddress"></a>
<a id="schema_Address"></a>
<a id="tocSaddress"></a>
<a id="tocsaddress"></a>

```json
{
  "id": 0,
  "default": true,
  "campus_branch": "四平路校区",
  "telephone": "string",
  "name": "string",
  "full_address": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||自增主键|
|default|boolean|false|none|是否为默认收货地址|none|
|campus_branch|string|true|none||所在校区|
|telephone|string|true|none|手机号|none|
|name|string|true|none|收货人姓名|none|
|full_address|string|true|none|详细地址|none|

#### 枚举值

|属性|值|
|---|---|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

<h2 id="tocS_Favor">Favor</h2>

<a id="schemafavor"></a>
<a id="schema_Favor"></a>
<a id="tocSfavor"></a>
<a id="tocsfavor"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "item_id": 0,
  "collect_time": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|user_id|integer|true|none||收藏者的学号|
|item_id|integer|true|none||物品ID|
|collect_time|string|true|none||收藏时间|

<h2 id="tocS_Review">Review</h2>

<a id="schemareview"></a>
<a id="schema_Review"></a>
<a id="tocSreview"></a>
<a id="tocsreview"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "publish_time": "string",
  "feedback_content": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|user_id|integer|true|none||发布者的学号|
|publish_time|string|true|none||发布时间|
|feedback_content|string¦null|false|none||详细反馈|

<h2 id="tocS_User_Management">User_Management</h2>

<a id="schemauser_management"></a>
<a id="schema_User_Management"></a>
<a id="tocSuser_management"></a>
<a id="tocsuser_management"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "ban_time": "string",
  "ban_reason": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||none|
|user_id|integer|true|none||none|
|ban_time|string|true|none||none|
|ban_reason|string|true|none||none|

<h2 id="tocS_Address_info">Address_info</h2>

<a id="schemaaddress_info"></a>
<a id="schema_Address_info"></a>
<a id="tocSaddress_info"></a>
<a id="tocsaddress_info"></a>

```json
{
  "campus_branch": "string",
  "telephone": "string",
  "name": "string",
  "full_address": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|campus_branch|string|true|none||none|
|telephone|string|true|none||none|
|name|string|true|none||none|
|full_address|string|true|none||none|

<h2 id="tocS_Feedback">Feedback</h2>

<a id="schemafeedback"></a>
<a id="schema_Feedback"></a>
<a id="tocSfeedback"></a>
<a id="tocsfeedback"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "publish_time": "string",
  "kind": 0,
  "state": 0,
  "feedback_content": "string",
  "reply_content": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||none|
|user_id|integer|true|none||none|
|publish_time|string|true|none||none|
|kind|integer|true|none||none|
|state|integer|true|none||none|
|feedback_content|string|true|none||none|
|reply_content|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|kind|0|
|kind|1|
|kind|2|
|kind|3|
|kind|4|
|kind|5|
|state|0|
|state|1|
|state|-1|

<h2 id="tocS_Order_State_Item">Order_State_Item</h2>

<a id="schemaorder_state_item"></a>
<a id="schema_Order_State_Item"></a>
<a id="tocSorder_state_item"></a>
<a id="tocsorder_state_item"></a>

```json
{
  "id": 0,
  "order_id": 0,
  "user_review_id": 0,
  "op_user_review_id": 0,
  "cancel_user": 0,
  "cancel_reason": "string"
}

```

    订单状态为未确认 0时：有两个变量：买方已确认 卖方已确认。当双方都确认时，订单状态转为3。
    订单状态处于未确认 0时：可以发起取消。取消立即生效。库存恢复。扣除发起方信誉分。订单状态转为已关闭（-1）。
    订单状态处于已完成 2时：有两个变量：买方评价的评价id（foreign key review_id on default null）,卖方评价id。
    订单状态处于已关闭 -1时：有两个变量：取消方（user_id or 管理员(80000000)），详细取消原因（取消方填，可无）

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|order_id|integer|true|none||订单编号|
|user_review_id|integer¦null|false|none||Review的外键，发起方对应的评价内容的ID|
|op_user_review_id|integer¦null|false|none||Review的外键，对方对应的评价内容的ID|
|cancel_user|integer¦null|false|none||取消方ID, 可由发起方、对方或管理员取消|
|cancel_reason|string¦null|false|none||取消原因|

<h2 id="tocS_User">User</h2>

<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
  "id": 9999999,
  "username": "string",
  "email": "string",
  "state": 0,
  "score": 100,
  "gender": "男",
  "user_no_is_published": false,
  "user_no": "string",
  "telephone_is_published": false,
  "telephone": "string",
  "wechat_is_published": false,
  "wechat": "string",
  "qq_is_published": false,
  "qq_number": "string",
  "campus_is_published": false,
  "campus_branch": "四平路校区",
  "dormitory_is_published": false,
  "dormitory": "友园7号楼",
  "name_is_published": false,
  "name": "string",
  "major_is_published": false,
  "major": "string",
  "password_hash": "string"
}

```

用户表

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||none|
|username|string|true|none||用户名|
|email|string|true|none||邮箱|
|state|integer|true|none||用户状态|
|score|integer|true|none||信誉分|
|gender|string|true|none||性别|
|user_no_is_published|boolean|true|none||是否公开学号|
|user_no|string|false|none||学工号|
|telephone_is_published|boolean|true|none||是否公开电话|
|telephone|string¦null|false|none||电话|
|wechat_is_published|boolean|true|none||是否公开微信|
|wechat|string¦null|false|none||微信号|
|qq_is_published|boolean|true|none||是否公开qq|
|qq_number|string¦null|false|none||QQ号|
|campus_is_published|boolean|true|none||是否公开所在校区|
|campus_branch|string|false|none||所在校区|
|dormitory_is_published|boolean|true|none||是否公开所在宿舍|
|dormitory|string¦null|false|none||所在宿舍|
|name_is_published|boolean|true|none||是否公开姓名|
|name|string¦null|false|none||真实姓名|
|major_is_published|boolean|true|none||是否公开专业|
|major|string¦null|false|none||专业名|
|password_hash|string|true|none||密码的hash值|

#### 枚举值

|属性|值|
|---|---|
|state|0|
|state|1|
|state|-1|
|gender|男|
|gender|女|
|gender|保密|
|campus_branch|四平路校区|
|campus_branch|嘉定校区|
|campus_branch|沪西校区|
|campus_branch|沪北校区|

<h2 id="tocS_标准API接口">标准API接口</h2>

<a id="schema标准api接口"></a>
<a id="schema_标准API接口"></a>
<a id="tocS标准api接口"></a>
<a id="tocs标准api接口"></a>

```json
{
  "success": true,
  "statusCode": 200,
  "message": "string",
  "data": {}
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|success|boolean|true|none||none|
|statusCode|integer|true|none||none|
|message|string|true|none||none|
|data|object|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|statusCode|200|
|statusCode|201|
|statusCode|400|
|statusCode|401|
|statusCode|404|
|statusCode|500|

<h2 id="tocS_Order_Item">Order_Item</h2>

<a id="schemaorder_item"></a>
<a id="schema_Order_Item"></a>
<a id="tocSorder_item"></a>
<a id="tocsorder_item"></a>

```json
{
  "id": 0,
  "order_id": 0,
  "quantity": 0,
  "price": 0,
  "item_id": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|order_id|integer|true|none||外键，订单的ID|
|quantity|integer|true|none||购买数量此项乘对应商品/悬赏的单价，再与订单中其他物品相加等于订单中的总价|
|price|number|true|none||单价|
|item_id|integer|true|none||物品ID|

<h2 id="tocS_Order">Order</h2>

<a id="schemaorder"></a>
<a id="schema_Order"></a>
<a id="tocSorder"></a>
<a id="tocsorder"></a>

```json
{
  "id": 0,
  "user_id": 0,
  "payment": 0,
  "state": -1,
  "create_time": "string",
  "confirm_time": "string",
  "end_time": "string",
  "close_time": "string",
  "note": "string",
  "campus_branch": "string",
  "telephone": "string",
  "name": "string",
  "full_address": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|none||ID|
|user_id|integer|true|none||订单发起者的学号|
|payment|number|true|none||总价|
|state|integer|true|none||订单状态|
|create_time|string|true|none||创建时间|
|confirm_time|string¦null|false|none||双方确认时间|
|end_time|string¦null|false|none||完成时间|
|close_time|string¦null|false|none||关闭时间（被一方取消）|
|note|string¦null|false|none||订单备注|
|campus_branch|string|true|none||none|
|telephone|string|true|none||none|
|name|string|true|none||none|
|full_address|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|state|-1|
|state|0|
|state|1|
|state|2|

