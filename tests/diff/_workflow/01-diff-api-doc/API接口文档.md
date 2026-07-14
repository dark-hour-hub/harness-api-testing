# RuoYi-Vue-Plus API 接口文档（增量）

## 项目信息

| 属性 | 值 |
|------|-----|
| **系统名称** | RuoYi-Vue-Plus |
| **Base URL** | `http://localhost:8080` |
| **框架** | Spring Boot 3.5.15 / Java 21 / Sa-Token 1.45.0 + JWT |
| **数据库** | MySQL 8.0 + MyBatis-Plus 3.5.16 |
| **缓存** | Redis + Caffeine (Sa-Token 二级缓存) |
| **API 文档** | SpringDoc OpenAPI 2.8.17 |
| **认证方式** | Sa-Token JWT Simple，Header: `Authorization: Bearer {token}` |
| **接口加密** | 登录/注册接口使用 @ApiEncrypt (全局 API 加解密开关**已关闭**) |
| **验证码** | **已关闭** (`captcha.enable: false`)，登录接口无需验证码 |
| **文档版本** | v1.1 (增量) |
| **生成日期** | 2026-07-14 |
| **基线版本** | v1.0 |

---

## 测试账号

| 角色 | 用户名 | 密码 | 权限范围 |
|------|--------|------|----------|
| 超级管理员 | `admin` | `admin123` | 所有权限 (userId=1, role: super_admin) |
| 普通用户 | `test` | `666666` | 普通权限，受限 |

---

## 全局默认请求头

### 公开接口（无需认证）

| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Content-Type | String | ✅ | 请求体格式，文件上传使用 `multipart/form-data` | `application/json` |

> 适用于：认证模块全部接口（/auth/**）、首页接口（GET /、GET /new）。

### 认证接口（需要认证）

在公开接口基础上额外携带：

| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Authorization | String | ✅ | `Bearer {token}`，由登录接口获取 | `Bearer eyJhbG...` |
| clientid | String | ✅ | 客户端 ID，必须与登录时使用的 clientId 一致 | `e5cd7e4891bf95d1d19206ce24a7b32e` |

> 后续各模块文档中，"请求头: [公开]" / "请求头: [认证]" 分别引用上述模板。

---

## 响应包装说明

所有接口响应均经过统一的包装类处理，以下为框架级定义。

### R\<T\> — 非分页响应

| 字段路径 | 类型 | 可空 | 说明 | 示例值 |
|----------|------|:---:|------|--------|
| code | Integer | 否 | 业务状态码，200=成功，500=失败，601=警告 | `200` |
| msg | String | 否 | 业务消息 | `"操作成功"` |
| data | T | 是 | 业务数据（泛型），无数据时为 `null` | `{...}` |

### TableDataInfo\<T\> — 分页响应

| 字段路径 | 类型 | 可空 | 说明 | 示例值 |
|----------|------|:---:|------|--------|
| code | Integer | 否 | 固定值 | `200` |
| msg | String | 否 | 固定值 | `"查询成功"` |
| rows | List\<T\> | 否 | 当前页数据列表 | `[{...}]` |
| total | Long | 否 | 总记录数 | `100` |

---

## 权限体系

- **权限模型**: RBAC
- **超级管理员**: `admin` (userId=1, role: super_admin) — 拥有所有权限，查看所有数据
- **权限标识格式**: `{模块}:{资源}:{操作}` (如 `system:user:list`, `system:user:add`, `system:user:edit`, `system:user:remove`, `system:user:query`, `system:user:export`, `system:user:import`)
- **数据权限**: 按部门数据权限 (5级: 全部数据权限 / 自定义数据权限 / 本部门数据权限 / 本部门及以下数据权限 / 仅本人数据权限)
- **角色权限**: 支持 `@SaCheckRole` 注解（如超管角色 `super_admin`、租户管理员角色 `tenant_admin`）

---

## 变更模块概览（仅受影响模块）

| 模块 | 路由前缀 | 变更接口数 | 说明 | 文档链接 |
|------|---------|:---:|------|----------|
| 首页 | `/` | 1 新增 | 新增 `GET /new` 欢迎接口 | [modules/06-首页.md](modules/06-首页.md) |
| 系统管理 — 岗位管理 + 字典管理 | `/system/post`, `/system/dict` | 4 修改 | 岗位列表/详情/选项/导出响应体新增 `address` 字段 | [modules/02-系统管理-part4.md](modules/02-系统管理-part4.md) |
| 系统管理 — 用户管理 + 个人中心 | `/system/user`, `/system/user/profile` | 1 修改 | 用户信息查询中岗位数据含 `address` 字段 | [modules/02-系统管理-part1.md](modules/02-系统管理-part1.md) |
| 工作流管理 — 任务管理 + 请假示例 | `/workflow/task`, `/workflow/leave` | 3 修改 | 异常跳过条件扩展 + 间接影响 | [modules/05-工作流管理-part3.md](modules/05-工作流管理-part3.md) |

> **增量原则**：仅列出受影响的模块。未变更模块（认证、角色管理、菜单管理、部门管理、通知公告、参数配置、客户端管理、租户管理、OSS、监控管理、代码生成、工作流分类/定义/实例/Spel）参见基线文档。

---

## 框架/配置变更

| 变更项 | 变更前 | 变更后 | 测试影响 |
|------|------|------|------|
| Java 版本 | 17 | 21 | 虚拟线程等新特性可用；需确认测试环境 JDK ≥ 21 |
| 验证码 (`captcha.enable`) | `true` | `false` | 登录测试无需获取验证码，简化测试流程 |
| API 接口加密 (`api-decrypt.enabled`) | `true` | `false` | 请求体无需 AES 加密，可直接传明文 JSON |
| 数据库地址 | `localhost:3306` | `180.76.180.32:3306` | 远程数据库，注意网络延迟和权限 |
| Redis 地址 | `localhost:6379` | `180.76.180.32:6379` | 远程 Redis，确认密码 `123456` |

---

## 已知问题与注意事项

| # | 问题 | 影响接口 | 说明 | 建议 |
|---|------|---------|------|------|
| 1 | 登录接口加密 | POST /auth/login, POST /auth/register | 请求体使用 @ApiEncrypt 加密，需先获取加密密钥或临时关闭加密 | 测试时可在配置中关闭 `api-decrypt.enabled`（已关闭） |
| 2 | 验证码已关闭 | POST /auth/login | `captcha.enable: false`，登录接口无需验证码 | 测试正常登录流程即可 |
| 3 | JWT 密钥硬编码 | 所有认证接口 | `jwt-secret-key` 硬编码在 application.yml，生产环境需替换 | 安全审计建议 |
| 4 | 跨域全放开 | 所有接口 | `addAllowedOriginPattern("*")` 允许所有来源 | 生产环境需限制 |
| 5 | `SysPostVo.address` 疑似调试代码 | 岗位相关接口 | `address` 字段硬编码为 `"LosAngeles"`，非数据库字段 | 正式上线前确认字段用途 |
| 6 | `GET /new` 无鉴权 | GET /new | 类级 `@SaIgnore` 使该端点无需认证即可访问 | 确认是否为预期行为 |
| 7 | 工作流条件跳过扩展 | /workflow/task/** | `NULL_SKIP_TYPE` 异常被静默跳过而非抛出 | 确认跳过逻辑在业务上合理 |

---

*文档基于 RuoYi-Vue-Plus 5.6.2 后端源码生成 · v1.1 (增量) · 2026-07-14*
