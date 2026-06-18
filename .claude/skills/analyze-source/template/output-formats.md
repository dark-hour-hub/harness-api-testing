# 输出格式模板

分析完成后各输出文件的格式定义。

---

## 1. API 定义 (YAML)

用于描述单个 API 的完整信息，包括请求体和响应字段。

```yaml
apis:
  - method: POST
    path: /api/users
    controller: UserController
    method_name: createUser
    description: 创建用户
    parameters:
      - name: user
        type: UserDTO
        location: @RequestBody
    return_type: Result<UserVO>
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
        roles:
          type: array
          items:
            type: string
          description: 角色列表
    response_fields:
      code:
        type: integer
        description: 状态码，200表示成功
      message:
        type: string
        description: 响应消息
      data:
        type: object
        description: 响应数据
        properties:
          id:
            type: integer
            description: 用户ID
          username:
            type: string
            description: 用户名
          email:
            type: string
            description: 邮箱
          createTime:
            type: string
            format: datetime
            description: 创建时间
```

---

## 2. 分析报告 (Markdown)

输出到 `tests/baseline/specs/{module}/*-analysis.md`。

```markdown
# 模块分析报告

## 技术栈

- 后端：Java Spring Boot 2.7.x
- 前端：Vue 3 + Element Plus
- 数据库：MySQL

## 微服务

| 服务名 | 端口 | 描述 |
|--------|------|------|
| user-service | 8081 | 用户服务 |
| course-service | 8082 | 课程服务 |

## API 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /api/users | 创建用户 | ROLE_ADMIN |
| GET | /api/users/{id} | 获取用户 | ROLE_USER |

## 前端页面

| 路径 | 组件 | 描述 |
|------|------|------|
| /login | Login.vue | 登录页 |
| /dashboard | Dashboard.vue | 控制台 |

## 认证机制

- 类型：JWT
- Token 过期时间：2 小时
```

---

## 3. 规格文件 (YAML)

输出到 `tests/baseline/specs/{module}/*-spec.yaml`。

```yaml
module: user
version: "0516"
analyzed_at: "2026-06-09T10:00:00"

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
        username:
          type: string
          required: true
        email:
          type: string
          required: true
    response:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
```

---

## 4. 接口文件 apis.json (JSON)

输出到 `tests/baseline/_workflow/02-analysis-plan/apis.json`。

`apis.json` 必须包含每个 API 的 `request_body` 和 `response_fields` 定义，获取方式：
- 解析 Controller 方法参数上的 `@RequestBody` 注解，找到对应的 DTO 类
- 解析 DTO 类的字段定义，包括类型、是否必填、校验规则
- 解析返回值 `Result<T>` 中的 T 类型（VO 类）获取响应字段

```json
{
  "modules": {
    "user": {
      "name": "用户管理模块",
      "apis": [
        {
          "method": "POST",
          "path": "/api/users",
          "description": "创建用户",
          "requires_auth": true,
          "permissions": ["ROLE_ADMIN"],
          "request_body": {
            "type": "object",
            "required": ["username", "password"],
            "properties": {
              "username": {"type": "string", "description": "用户名", "maxLength": 32},
              "password": {"type": "string", "description": "密码", "minLength": 6, "maxLength": 128},
              "email": {"type": "string", "description": "邮箱", "format": "email"}
            }
          },
          "response_fields": {
            "code": {"type": "integer", "description": "状态码"},
            "message": {"type": "string", "description": "消息"},
            "data": {
              "type": "object",
              "properties": {
                "id": {"type": "integer", "description": "用户ID"},
                "username": {"type": "string", "description": "用户名"},
                "email": {"type": "string", "description": "邮箱"}
              }
            }
          }
        }
      ]
    },
    "course": {
      "apis": []
    }
  },
  "auth": {
    "type": "JWT",
    "login_endpoint": "/api/auth/login",
    "token_header": "Authorization",
    "token_prefix": "Bearer"
  },
  "services": {
    "user-service": {
      "type": "backend",
      "port": 8080,
      "base_url": "http://localhost:8080"
    }
  },
  "analyzed_at": "2026-06-10T10:00:00"
}
```

---

## 5. 前端页面 (YAML)

用于描述 Vue 页面及其元素。

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

用于描述系统的认证配置。

```yaml
auth:
  auth_type: JWT
  login_endpoint: /api/auth/login
  token_header: Authorization
  token_prefix: Bearer
  token_field: token
  refresh_endpoint: /api/auth/refresh
```
