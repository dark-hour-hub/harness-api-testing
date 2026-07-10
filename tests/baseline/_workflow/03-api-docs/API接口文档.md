# Spring PetClinic API 接口文档

## 项目信息

| 属性 | 值 |
|------|-----|
| **系统名称** | Spring PetClinic |
| **Base URL** | `http://localhost:8080` |
| **框架** | Spring Boot 4.1.0 / Java 17 / Spring MVC (WebMVC) |
| **数据库** | H2 内存数据库（默认）/ MySQL / PostgreSQL + Spring Data JPA |
| **缓存** | Caffeine 本地缓存 + Spring Cache 抽象 |
| **API 文档** | 无（无 Swagger/Knife4j 依赖） |
| **认证方式** | 无（所有接口公开访问） |
| **接口加密** | 无 |
| **文档版本** | v1.0 |
| **生成日期** | 2026-07-10 |

---

## 测试账号

| 角色 | 用户名 | 密码 | 权限范围 |
|------|--------|------|----------|
| 无需认证 | N/A | N/A | 所有接口无需登录，无需携带任何认证信息 |

---

## 全局默认请求头

### 所有接口（无需认证）

| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Content-Type | String | ✅ | 表单提交使用 `application/x-www-form-urlencoded`；JSON 请求使用 `application/json` | `application/x-www-form-urlencoded` |

> 该项目无认证机制，所有接口均公开访问，无需 Authorization 或其他认证头。

---

## 响应包装说明

> **该项目无统一响应包装类。** Spring PetClinic 是传统 Spring MVC 服务端渲染应用，未使用 RuoYi 风格的 R/TableDataInfo 包装。

### HTML 视图响应（大部分接口）

大部分接口返回 Thymeleaf 渲染的 HTML 页面：

| 场景 | HTTP 状态码 | 响应体 |
|------|:---:|------|
| 成功 | `200` | 渲染后的 HTML 页面 |
| 表单校验失败 | `200` | 返回原表单页面，显示校验错误信息 |
| 资源不存在 | `500` | 错误页面（IllegalArgumentException） |

成功操作后通过 `RedirectAttributes.addFlashAttribute` 传递提示消息（`message` 或 `error`），然后 redirect 到目标页面。

### JSON 响应（仅 GET /vets）

`GET /vets` 使用 `@ResponseBody` 注解，直接返回 JSON：

| 字段路径 | 类型 | 说明 | 示例值 |
|----------|------|------|--------|
| vetList | Array\<Vet\> | 兽医列表 | `[{"id":1,"firstName":"James",...}]` |
| vetList[].id | Integer | 兽医ID | `1` |
| vetList[].firstName | String | 名字 | `"James"` |
| vetList[].lastName | String | 姓氏 | `"Carter"` |
| vetList[].specialties | Array\<Specialty\> | 专业领域列表 | `[{"id":1,"name":"radiology"}]` |
| vetList[].nrOfSpecialties | Integer | 专业领域数量 | `1` |

---

## 权限体系

- **权限模型**: 无权限控制
- **超级管理员**: N/A
- **权限标识格式**: N/A
- **数据权限**: N/A

---

## 模块概览

| 模块 | 路由前缀 | 接口数量 | 说明 | 文档链接 |
|------|---------|:---:|------|----------|
| 首页 | `/` | 1 | 欢迎页 | [modules/01-首页.md](modules/01-首页.md) |
| 兽医管理 | `/vets` | 1 | 兽医列表（JSON API） | [modules/02-兽医管理.md](modules/02-兽医管理.md) |
| 客户管理 | `/owners` | 13 | 客户 CRUD + 宠物管理 + 就诊记录 | [modules/03-客户管理.md](modules/03-客户管理.md) |

> 各模块的接口明细（请求参数、响应结构、错误码、业务规则）见对应模块文档。实体类定义见 `entities/` 目录。

---

## 已知问题与注意事项

| # | 问题 | 影响接口 | 说明 | 建议 |
|---|------|---------|------|------|
| 1 | 无统一响应格式 | 所有 | 接口返回 HTML 或直接 JSON（仅 /vets），无 code/msg 业务状态码 | 测试时以 HTTP 状态码 + 页面内容/JSON 结构作为断言依据 |
| 2 | 默认 H2 内存数据库 | 所有 | 重启后数据重置为初始 seed 数据 | 测试前确认数据状态，或切换至 MySQL/PostgreSQL profile |
| 3 | 无认证机制 | 所有 | 所有接口可匿名直接访问 | 生产环境应添加认证层 |
| 4 | 表单 CSRF | 所有 POST | Spring MVC 表单可能启用 CSRF 保护 | 测试 POST 接口时注意 CSRF token（如启用） |

---

*文档基于 `D:\java\project\spring-petclinic` 源码扫描生成 · v1.0 · 2026-07-10*
