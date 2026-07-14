# 认证机制分析报告

**生成时间**: 2026-07-14
**分析项目数**: 1

---

## 项目：RuoYi-Vue-Plus

### 一、认证方式

| 属性 | 值 |
|------|-----|
| 认证类型 | `sa-token` |
| 认证描述 | 基于 Sa-Token 1.45.0 + JWT（简单模式）的无状态认证，SaTokenDao 使用 Caffeine（5s 本地缓存）+ Redis（持久存储）二级缓存，支持多租户、多用户类型、多设备类型 |

### 二、请求头要求

| 请求头名称 | 是否必填 | 条件 | 用途 |
|-----------|---------|------|------|
| Authorization | 是 | 除白名单外所有路径 | 认证令牌，格式 `Bearer {token}` |
| clientid | 条件必填 | 带 token 的非白名单路径 | 客户端 ID，必须与 token 中存储的 clientId 一致，不一致则返回 401 |
| encrypt-key | 否 | 登录等加密接口 | API 加密头标识（当前全局加密关闭，仅登录接口通过 `@ApiEncrypt` 开启） |

> **注意**：`clientid` 同时从 Header 和请求参数中读取。Sa-Token 配置了同时从 Header 和请求体读取 token（`is-read-header: true`, `is-read-body: true`），Cookie 读取已关闭。

### 三、登录接口

| 属性 | 值 |
|------|-----|
| 接口路径 | `POST /auth/login` |
| 请求体格式 | JSON（加密，`@ApiEncrypt`） |
| 认证豁免 | `@SaIgnore` 注解标记 |

**必填字段**（基于 `LoginBody` + `PasswordLoginBody`）：

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| clientId | string | 必填 | 客户端 ID（如 `e5cd7e4891bf95d1d19206ce24a7b32e`） |
| grantType | string | 必填 | 授权类型（如 `password`、`sms`、`email`、`xcx`） |
| username | string | 必填（password 模式） | 用户名，2-30 字符 |
| password | string | 必填（password 模式） | 密码，5-30 字符 |
| tenantId | string | 可选 | 租户 ID（如 `000000`） |
| code | string | 可选 | 验证码（当前全局关闭验证码） |
| uuid | string | 可选 | 验证码唯一标识 |

**其他登录方式**（继承 `LoginBody`）：
- `SmsLoginBody` — 短信验证码登录
- `EmailLoginBody` — 邮箱验证码登录
- `XcxLoginBody` — 小程序登录
- `SocialLoginBody` — 第三方社交登录

**登录响应**：返回 `LoginVo` 对象（包含 `token` 字段）。

**其他认证接口**：
- `GET /auth/binding/{source}` — 获取第三方登录跳转 URL
- `POST /auth/social/callback` — 第三方登录回调绑定（需要 token）
- `DELETE /auth/unlock/{socialId}` — 取消第三方授权（需要 token）
- `POST /auth/logout` — 退出登录
- `POST /auth/register` — 用户注册
- `GET /auth/tenant/list` — 获取租户列表（限流 60s/20次/IP）

### 四、拦截器/过滤器链

请求链路（按顺序）：

**过滤器链（Filter）**：

```
1. CorsFilter (org.springframework.web.filter.CorsFilter)
   类型: Filter
   路径: /**
   排除: 无
   动作: 跨域处理，允许所有来源/请求头/方法。与认证无关。

2. RepeatableFilter (org.dromara.common.web.filter.RepeatableFilter)
   类型: Filter（extends OncePerRequestFilter）
   路径: /**
   动作: 包装 HttpServletRequest 为 RepeatedlyRequestWrapper，使请求体可重复读取。与认证无关。

3. XssFilter (org.dromara.common.web.filter.XssFilter)
   类型: Filter（extends OncePerRequestFilter）
   路径: /**
   排除: /system/notice, /warm-flow/save-json
   动作: XSS 过滤。与认证无关。

4. CryptoFilter (org.dromara.common.encrypt.filter.CryptoFilter)
   类型: Filter
   路径: /**
   动作: API 请求/响应加解密（当前全局开关关闭）。与认证无关。
```

**拦截器链（Interceptor）**：

```
5. SaInterceptor (cn.dev33.satoken.interceptor.SaInterceptor) [第一个拦截器]
   类型: HandlerInterceptor
   路径: /**
   排除: /*.html, /**/*.html, /**/*.css, /**/*.js, /favicon.ico, /error, /*/api-docs, /*/api-docs/**, /warm-flow-ui/config, /resource/sse
   动作: 认证核心检查
        (1) SaRouter.match(allUrls) — 匹配所有注册的 URL
        (2) StpUtil.checkLogin() — 校验是否登录（从 Authorization header 读取 Bearer token）
        (3) 校验 header/param 中的 clientid 与 token 中存储的 clientId 是否一致
        (4) 不一致则抛出 NotLoginException → 返回 401 "客户端ID与Token不匹配"
   必填头: [Authorization: Bearer {token}, clientid]

6. PlusWebInvokeTimeInterceptor (org.dromara.common.web.interceptor.PlusWebInvokeTimeInterceptor) [第二个拦截器]
   类型: HandlerInterceptor
   路径: 全局（由 ResourcesConfig 注册，无路径过滤）
   动作: 请求耗时统计 + 日志打印（脱敏敏感字段）。与认证无关。
```

**SaServletFilter（特殊 Filter）**：

```
7. SaServletFilter (Actuator 认证)
   类型: SaServletFilter
   路径: /actuator, /actuator/**
   动作: HTTP Basic 认证，校验 spring.boot.admin.client.username/password
   认证失败 → 返回 401
```

**WebSocket 拦截器**：

```
8. PlusWebSocketInterceptor
   类型: HandshakeInterceptor
   路径: /resource/websocket
   动作: WebSocket 握手前认证（检查 token + clientid 一致性）
```

### 五、权限模型

| 属性 | 值 |
|------|-----|
| 权限注解 | `@SaCheckPermission`、`@SaCheckRole`（Sa-Token 注解） |
| 权限粒度 | 权限字符串级（如 `@SaCheckPermission("workflow:leave:list")`），同时支持角色权限 |
| 说明 | `SaPermissionImpl` 实现 `StpInterface`，从 `LoginUser` 的 `menuPermission` 和 `rolePermission` 集合中获取权限列表。超级管理员（userId=1）拥有所有权限。权限注解广泛用于 Controller 方法上。 |

**异常处理**：全局 `SaTokenExceptionHandler`（`@RestControllerAdvice`）统一捕获：
- `NotLoginException` → HTTP 401 "认证失败，无法访问系统资源"
- `NotPermissionException` → HTTP 403 "没有访问权限，请联系管理员授权"
- `NotRoleException` → HTTP 403 "没有访问权限，请联系管理员授权"

### 六、白名单路径

| 路径 | 说明 |
|------|------|
| /*.html | 静态 HTML 文件 |
| /**/*.html | 所有 HTML 文件 |
| /**/*.css | 样式文件 |
| /**/*.js | JavaScript 文件 |
| /favicon.ico | 网站图标 |
| /error | 错误页面 |
| /*/api-docs | API 文档 |
| /*/api-docs/** | API 文档子路径 |
| /warm-flow-ui/config | 工作流 UI 配置 |
| /resource/sse | SSE 推送路径 |

> **注意**：`/auth/**` 路径也实际豁免认证（`AuthController` 类上标注了 `@SaIgnore`），但未出现在 `security.excludes` 配置中。`/auth/social/callback` 和 `/auth/unlock/{socialId}` 内部自行调用 `StpUtil.checkLogin()` 检查。

### 七、建议与注意事项

#### 测试建议
- **所有接口（除白名单外）需在请求头携带**：
  - `Authorization: Bearer {token}` — 认证令牌
  - `clientid: {clientId}` — 客户端 ID（必须与登录时使用的 `clientId` 一致）
- **测试前先调用 `POST /auth/login` 获取 token**，示例请求体（解密后）：
  ```json
  {
    "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
    "grantType": "password",
    "tenantId": "000000",
    "username": "admin",
    "password": "admin123"
  }
  ```
- **登录接口请求体已加密**（`@ApiEncrypt`），如需直接调用需先获取加密密钥或临时关闭接口加密。
- **Token 无固定过期时间**（`dynamic-active-timeout: true` 允许动态设置），需在实际测试中确认。
- **多端登录**：`is-concurrent: true` 允许同一账号多端登录，`is-share: false` 每次登录生成独立 token。
- **WebSocket 测试**需在握手请求中携带与 HTTP 接口相同的 Authorization header。

#### 安全提示
- **硬编码 JWT 密钥**：`jwt-secret-key: abcdefghijklmnopqrstuvwxyz` 硬编码在 application.yml 中，任何人都可以伪造 token。**强烈建议生产环境替换并通过环境变量注入。**
- **默认账户**：admin/admin123（超级管理员）、test/666666（普通用户），生产环境应立即修改。
- **验证码已关闭**：`captcha.enable: false`，登录接口无验证码保护，存在暴力破解风险。
- **数据库/Redis 密码明文**：配置文件中数据库和 Redis 密码以明文存储，建议使用加密配置或环境变量。
- **跨域全放开**：`addAllowedOriginPattern("*")` 允许所有来源，生产环境应限制具体域名。

#### 必填字段清单（接口测试）

| 场景 | 必填请求头/参数 |
|------|----------------|
| 密码登录 | Body: `clientId`, `grantType`, `username`, `password`; Header: 无认证头 |
| 业务接口调用 | Header: `Authorization: Bearer {token}`, `clientid` |
| Actuator 端点 | Header: `Authorization: Basic base64(username:password)` |
| WebSocket 连接 | Header: `Authorization: Bearer {token}`, `clientid` |
