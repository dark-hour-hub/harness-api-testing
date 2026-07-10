# _manifest.yaml 格式定义

结构化清单文件，下游 Skill 的输入合约。

## 完整格式

```yaml
system:
  name: "{系统名称}"
  base_url: "{http://localhost:8080}"
  framework: "{Spring Boot 3.5.15 / Java 21 / Sa-Token}"
  database: "{MySQL 8.0 + MyBatis-Plus}"
  cache: "{Redis + Caffeine}"
  api_doc: "{SpringDoc OpenAPI}"
  auth_type: "{Sa-Token JWT Simple}"
  auth_header: "Authorization: Bearer {token}"
  encryption: "{无}"

response_wrapper:
  class: R
  code_field: code       # 从 R.java 源码确认
  msg_field: msg         # 从 R.java 源码确认
  success_code: 200      # R.ok() 的默认 code
  page_class: TableDataInfo
  page_rows_field: rows
  page_total_field: total

test_accounts:
  - role: admin
    username: admin
    password: admin123
    clientId: e5cd7e4891bf95d1d19206ce24a7b32e
    grantType: password
    tenantId: "000000"
    description: 超级管理员

auth:
  white_list: ["/*.html", "/**/*.html", "/**/*.css", "/**/*.js", "/favicon.ico", "/error", "/*/api-docs", "/*/api-docs/**", "/warm-flow-ui/config", "/resource/sse", "/auth/**", "/"]
  public_headers:
    - name: Content-Type
      type: String
      required: true
      example: application/json
  auth_headers:
    - name: Authorization
      type: String
      required: true
      example: "Bearer eyJhbG..."
    - name: clientid
      type: String
      required: true
      example: e5cd7e4891bf95d1d19206ce24a7b32e

permission_model:
  type: RBAC
  super_admin: "admin (角色: super_admin)"
  format: "{模块}:{资源}:{操作}"
  data_permission: 按部门数据权限

modules:
  - name: 认证模块
    prefix: /auth
    file: "01-认证模块.md"
    interface_count: 11
    controllers:
      - class: AuthController
        package: org.dromara.web.controller
    services:
      - class: SysLoginService
        package: org.dromara.system.service.impl
    dtos: [LoginBody, PasswordLoginBody, RegisterBody]
    vos: [LoginVo, TenantListVo]
    routes:
      - method: POST
        path: /auth/login
        summary: 用户登录
        request_body: LoginBody
        response_type: R<LoginVo>
        response_structure: single
        auth: false
        permission: null
        special: ["@RateLimiter"]
      # ...
    split_plan: null

  - name: 系统管理
    prefix: /system
    file: "02-系统管理.md"
    interface_count: 92
    controllers:
      - class: SysUserController
        package: org.dromara.system.controller
      # ... 更多 Controller
    services:
      - class: SysUserServiceImpl
        package: org.dromara.system.service.impl
      # ...
    dtos: [SysUserBo, SysUserDto, ...]
    vos: [SysUserVo, ...]
    routes: [...]
    split_plan:
      - part: 1
        file: "02-系统管理-part1.md"
        route_indices: [0..14]
      - part: 2
        file: "02-系统管理-part2.md"
        route_indices: [15..29]
      # ...
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `system` | 系统基本信息 |
| `response_wrapper` | 响应包装类信息 |
| `test_accounts` | 测试账号列表 |
| `auth` | 认证相关配置（白名单、请求头） |
| `permission_model` | 权限体系说明 |
| `modules` | 各模块详情列表 |
| `modules[].controllers` | 该模块涉及的 Controller 类 |
| `modules[].services` | 该模块涉及的 Service 类 |
| `modules[].dtos` | 该模块使用的请求 DTO 类名 |
| `modules[].vos` | 该模块使用的响应 VO 类名 |
| `modules[].routes` | 该模块所有路由详情 |
| `modules[].split_plan` | 接口数量超过15时拆分方案 |
