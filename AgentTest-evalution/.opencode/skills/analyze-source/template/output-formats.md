# 输出格式模板

分析完成后各输出文件的格式定义。

---

## 1. API 定义

用于描述单个 API 的完整信息。

```yaml
method: POST
path: /api/users
controller: UserController
description: 创建用户
requires_auth: true
permissions:
  - ROLE_ADMIN
request_body:
  type: object
  required:
    - username
    - password
  properties:
    username:
      type: string
      required: true
      description: 用户名
      maxLength: 32
    password:
      type: string
      required: true
      description: 密码
      minLength: 6
      maxLength: 128
    email:
      type: string
      required: false
      description: 邮箱
      format: email
response_fields:
  code:
    type: integer
    description: 状态码
  message:
    type: string
    description: 响应消息
  data:
    type: object
    properties:
      id: { type: integer, description: 用户ID }
      username: { type: string, description: 用户名 }
required_headers:
  Authorization:
    type: string
    required: true
    description: Bearer token
    source: ShiroFilter
  X-Tenant-Id:
    type: string
    required: true
    description: 租户ID
    source: TenantInterceptor
```

---

## 2. 分析报告 (Markdown)

输出到 `tests/baseline/specs/{module}/*-analysis.md`。

```markdown
# 模块分析报告

## 技术栈

- 后端：Java Spring Boot
- 前端：Vue 3 + Element Plus
- 数据库：MySQL

## 微服务

| 服务名 | 端口 | 描述 |
|--------|------|------|
| user-service | 8081 | 用户服务 |

## API 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /api/users | 创建用户 | ROLE_ADMIN |
| GET | /api/users/{id} | 获取用户 | ROLE_USER |

## 前端页面

| 路径 | 组件 | 描述 |
|------|------|------|
| /login | Login.vue | 登录页 |

## 认证机制

- 类型：JWT
- Token 过期时间：2 小时

## 拦截器/请求头

| 拦截器 | 路径前缀 | 必填 Header | 可选 Header |
|--------|----------|-------------|-------------|
| ShiroFilter | /api/* | Authorization | - |
| TenantInterceptor | /api/* | X-Tenant-Id | X-Request-Id |
```

---

## 3. 规格文件 (YAML)

输出到 `tests/baseline/specs/{module}/*-spec.yaml`。

```yaml
module: user
version: "<version>"
analyzed_at: "<timestamp>"

apis:
  - id: API_USER_CREATE
    method: POST
    path: /api/users
    description: 创建用户
    requires_auth: true
    permissions: [ROLE_ADMIN]
    request:
      type: object
      properties:
        username: { type: string, required: true }
        email: { type: string, required: true }
    response:
      type: object
      properties:
        id: { type: integer }
        username: { type: string }
```

---

## 4. 接口文件 apis.json

输出到 `tests/baseline/_workflow/02-analysis-plan/apis.json`。

扁平化结构，每个 API 携带所属模块信息：

```json
{
  "apis": [
    {
      "module": "user",
      "method": "POST",
      "path": "/api/users",
      "description": "创建用户",
      "requires_auth": true,
      "permissions": ["ROLE_ADMIN"],
      "request_body": {
        "type": "object",
        "required": ["username", "password"],
        "properties": {
          "username": { "type": "string", "description": "用户名", "maxLength": 32 },
          "password": { "type": "string", "description": "密码", "minLength": 6, "maxLength": 128 }
        }
      },
      "response_fields": {
        "code": { "type": "integer", "description": "状态码" },
        "message": { "type": "string", "description": "消息" },
        "data": {
          "type": "object",
          "properties": {
            "id": { "type": "integer", "description": "用户ID" },
            "username": { "type": "string", "description": "用户名" }
          }
        }
      },
      "required_headers": {
        "Authorization": {
          "type": "string",
          "required": true,
          "description": "Bearer token",
          "source": "ShiroFilter"
        },
        "X-Tenant-Id": {
          "type": "string",
          "required": true,
          "description": "租户ID",
          "source": "TenantInterceptor"
        }
      }
    }
  ],
  "auth": {
    "type": "JWT",
    "login_endpoint": "/api/auth/login",
    "token_header": "Authorization",
    "token_prefix": "Bearer"
  },
  "interceptors": [
    {
      "name": "ShiroFilter",
      "type": "Filter",
      "path_prefix": "/api/*",
      "required_headers": ["Authorization"],
      "optional_headers": []
    },
    {
      "name": "TenantInterceptor",
      "type": "HandlerInterceptor",
      "path_prefix": "/api/*",
      "required_headers": ["X-Tenant-Id"],
      "optional_headers": ["X-Request-Id"]
    }
  ],
  "analyzed_at": "<timestamp>"
}
```

---

## 5. 前端页面 (YAML)

```yaml
pages:
  - path: /login
    component: Login.vue
    name: 登录页
    elements:
      - selector: input[placeholder*="用户名"]
        type: input
        label: 用户名
      - selector: button[type="submit"]
        type: button
        label: 登录
    requires_auth: false
```

---

## 6. 认证机制 (YAML)

```yaml
auth:
  auth_type: JWT
  login_endpoint: /api/auth/login
  token_header: Authorization
  token_prefix: Bearer

interceptors:
  - name: ShiroFilter
    type: Filter
    path_prefix: /api/*
    required_headers:
      - Authorization
    optional_headers: []
  - name: TenantInterceptor
    type: HandlerInterceptor
    path_prefix: /api/*
    required_headers:
      - X-Tenant-Id
    optional_headers:
      - X-Request-Id
```

---

## 7. 生成计划 (Markdown)

输出到 `tests/baseline/_workflow/02-analysis-plan/generation-plan.md`。

```markdown
# 源码分析计划

**模块**: <module_name>
**生成时间**: <timestamp>
**分析方式**: CodeGraph 深度源码分析

---

## 一、分析范围

| 类型 | 数量 | 说明 |
|------|------|------|
| 后端源码 | <N> | Java/Python/Node.js 源码目录 |
| Controller | <N> | 控制器数量 |
| API 接口 | <N> | 接口数量 |
| DTO/VO 类 | <N> | 请求体和响应体结构 |

## 二、技术栈

| 类型 | 框架 | 说明 |
|------|------|------|
| 后端 | <框架> | <版本> |
| 前端 | <框架> | <版本> |
| 数据库 | <数据库> | <版本> |
| 认证框架 | <框架> | <说明> |

## 三、校验规则提取

从代码中提取的字段校验规则（用于生成边界值用例）：

| 字段 | 类型 | 必填 | 校验规则 | 来源 |
|------|------|------|----------|------|
| username | string | true | maxLength=32, minLength=3 | @Length |
| email | string | false | format=email | @Email |
| age | integer | false | min=0, max=150 | @Min/@Max |

## 四、错误消息追踪

从代码追踪的真实错误消息（用于生成反向用例断言）：

| 场景 | Code | Message | 追踪路径 |
|------|------|---------|----------|
| 用户名为空 | 500 | 用户名不能为空 | Controller → @NotBlank |
| 邮箱格式错误 | 500 | 邮箱格式不正确 | Controller → @Email |
| 资源不存在 | 404 | 请求地址不存在 | GlobalExceptionHandler |

## 五、输出文件

| 文件 | 路径 |
|------|------|
| 分析报告 | tests/baseline/specs/{module}/*-analysis.md |
| 规格文件 | tests/baseline/specs/{module}/*-spec.yaml |
| 接口文件 | tests/baseline/_workflow/02-analysis-plan/apis.json |
| 生成计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md |

## 六、下一步

使用 `test-case-generator` skill 生成测试用例 YAML。
```