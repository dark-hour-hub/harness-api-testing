# EmailLoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EmailLoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.EmailLoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 邮件登录请求体，用于邮箱+邮箱验证码方式登录 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| email | `email` | string | ✅ | `@NotBlank(message="{user.email.not.blank}")`, `@Email(message="{user.email.not.valid}")` | — | 邮箱地址，需符合 Email 格式 | `"admin@example.com"` |
| emailCode | `emailCode` | string | ✅ | `@NotBlank(message="{email.code.not.blank}")` | — | 邮箱验证码 | `"654321"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，固定为 `"email"` | `"email"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 图形验证码（邮件登录时通常不使用） | `""` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `""` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "email",
  "tenantId": "100000",
  "email": "admin@example.com",
  "emailCode": "654321"
}
```

---

*基于 `org.dromara.common.core.domain.model.EmailLoginBody` 源码生成 · 2026-07-14*
