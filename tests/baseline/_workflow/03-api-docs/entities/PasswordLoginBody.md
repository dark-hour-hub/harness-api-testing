# PasswordLoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `PasswordLoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.PasswordLoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 密码登录请求体，用于账号+密码+验证码方式登录 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| username | `username` | string | ✅ | `@NotBlank`, `@Length(min=2, max=30)` | — | 登录用户名 | `"admin"` |
| password | `password` | string | ✅ | `@NotBlank`, `@Length(min=5, max=30)` | — | 登录密码（明文传输，后端 BCrypt 校验） | `"admin123"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，固定为 `"password"` | `"password"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 图形验证码 | `"1234"` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `"a1b2c3d4e5f6"` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "password",
  "tenantId": "100000",
  "username": "admin",
  "password": "admin123",
  "code": "1234",
  "uuid": "a1b2c3d4e5f6"
}
```

---

*基于 `org.dromara.common.core.domain.model.PasswordLoginBody` 源码生成 · 2026-07-14*
