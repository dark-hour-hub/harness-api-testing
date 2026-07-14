# RuoYi-Vue-Plus API 接口文档

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
| **接口加密** | 登录/注册接口使用 @ApiEncrypt (全局 API 加解密开关关闭) |
| **文档版本** | v1.0 |
| **生成日期** | 2026-07-14 |

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

> 适用于：认证模块全部接口（/auth/**）、验证码接口、首页接口。

### 认证接口（需要认证）

在公开接口基础上额外携带：

| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Authorization | String | ✅ | `Bearer {token}`，由登录接口获取 | `Bearer eyJhbG...` |
| clientid | String | ✅ | 客户端 ID，必须与登录时使用的 clientId 一致 | `e5cd7e4891bf95d1d19206ce24a7b32e` |

> 后续各模块文档中，"请求头: [公开]" / "请求头: [认证]" 分别引用上述模板。每个模块文档开头有请求头引用块，列出本模块使用的请求头标识及其含义。

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

## 模块概览

| 模块 | 路由前缀 | 接口数量 | 说明 | 文档链接 |
|------|---------|:---:|------|----------|
| 认证模块 | `/auth` | 10 | 登录、注册、验证码、第三方登录、租户列表 | [modules/01-认证模块.md](modules/01-认证模块.md) |
| 系统管理 — 用户管理 + 个人中心 | `/system/user`, `/system/user/profile` | 18 | 用户CRUD、导入导出、授权角色、个人中心、头像上传 | [modules/02-系统管理-part1.md](modules/02-系统管理-part1.md) |
| 系统管理 — 角色管理 | `/system/role` | 15 | 角色CRUD、数据权限、用户分配、部门树 | [modules/02-系统管理-part2.md](modules/02-系统管理-part2.md) |
| 系统管理 — 菜单管理 + 部门管理 | `/system/menu`, `/system/dept` | 17 | 菜单CRUD、路由获取、部门CRUD、树形选择 | [modules/02-系统管理-part3.md](modules/02-系统管理-part3.md) |
| 系统管理 — 岗位管理 + 字典管理 | `/system/post`, `/system/dict` | 23 | 岗位CRUD、字典类型/数据CRUD、缓存刷新 | [modules/02-系统管理-part4.md](modules/02-系统管理-part4.md) |
| 系统管理 — 通知公告 + 参数配置 + 客户端管理 | `/system/notice`, `/system/config`, `/system/client` | 21 | 通知CRUD、参数配置CRUD、客户端管理CRUD | [modules/02-系统管理-part5.md](modules/02-系统管理-part5.md) |
| 系统管理 — 租户管理 + 租户套餐 + 社会化关系 | `/system/tenant`, `/system/social` | 20 | 租户CRUD、动态切换、套餐CRUD、社会化关系 | [modules/02-系统管理-part6.md](modules/02-系统管理-part6.md) |
| 系统管理 — OSS对象存储 + OSS配置 | `/resource/oss` | 11 | OSS上传/下载/删除、OSS配置CRUD | [modules/02-系统管理-part7.md](modules/02-系统管理-part7.md) |
| 监控管理 | `/monitor` | 14 | 登录日志、操作日志、在线用户、缓存监控 | [modules/03-监控管理.md](modules/03-监控管理.md) |
| 代码生成 | `/tool/gen` | 12 | 代码生成器：表导入、预览、下载、同步 | [modules/04-代码生成.md](modules/04-代码生成.md) |
| 工作流管理 — 流程分类 + 流程定义 | `/workflow/category`, `/workflow/definition` | 20 | 分类CRUD、定义CRUD、发布/复制/导入/导出 | [modules/05-工作流管理-part1.md](modules/05-工作流管理-part1.md) |
| 工作流管理 — 流程实例 + Spel表达式 | `/workflow/instance`, `/workflow/spel` | 18 | 实例查询/删除/挂起/撤销、表达式CRUD | [modules/05-工作流管理-part2.md](modules/05-工作流管理-part2.md) |
| 工作流管理 — 任务管理 + 请假示例 | `/workflow/task`, `/workflow/leave` | 24 | 任务启动/办理/驳回/委派/转办/加签/催办、请假CRUD | [modules/05-工作流管理-part3.md](modules/05-工作流管理-part3.md) |

> 各模块的接口明细（请求参数、响应结构、错误码、业务规则）见对应模块文档。实体类定义见 `entities/` 目录。

---

## 已知问题与注意事项

| # | 问题 | 影响接口 | 说明 | 建议 |
|---|------|---------|------|------|
| 1 | 登录接口加密 | POST /auth/login, POST /auth/register | 请求体使用 @ApiEncrypt 加密，需先获取加密密钥或临时关闭加密 | 测试时可在配置中关闭 `api-decrypt.enabled` |
| 2 | 验证码已关闭 | POST /auth/login | `captcha.enable: false`，登录接口无需验证码 | 测试正常登录流程即可 |
| 3 | JWT 密钥硬编码 | 所有认证接口 | `jwt-secret-key` 硬编码在 application.yml，生产环境需替换 | 安全审计建议 |
| 4 | 跨域全放开 | 所有接口 | `addAllowedOriginPattern("*")` 允许所有来源 | 生产环境需限制 |
| 5 | 多租户条件启用 | /system/tenant/** | SysTenantController 和 SysTenantPackageController 使用 `@ConditionalOnProperty(value = "tenant.enable")` | 仅当 `tenant.enable=true` 时可用 |
| 6 | 工作流条件启用 | /workflow/** | 所有工作流 Controller 使用 `@ConditionalOnEnable` 注解 | 仅当工作流功能启用时可用 |
| 7 | /auth/** 白名单 | /auth/** | AuthController 类级 @SaIgnore 豁免认证，但 /auth/social/callback 和 /auth/unlock/{socialId} 内部自行校验登录态 | 测试时注意区分 |
| 8 | 文档头部占位符未替换 | 02-系统管理-part5.md | 模块文档第3行 `clientid: {value}` 应为实际 clientId `e5cd7e4891bf95d1d19206ce24a7b32e` | 修正为实际值 |

---

*文档基于 RuoYi-Vue-Plus 5.6.2 后端源码生成 · v1.0 · 2026-07-14*
