# SmsLoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SmsLoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.SmsLoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 短信登录请求体，用于手机号+短信验证码方式登录 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| phonenumber | `phonenumber` | string | ✅ | `@NotBlank(message="{user.phonenumber.not.blank}")` | — | 手机号 | `"13800138000"` |
| smsCode | `smsCode` | string | ✅ | `@NotBlank(message="{sms.code.not.blank}")` | — | 短信验证码 | `"567890"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，固定为 `"sms"` | `"sms"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 图形验证码（短信登录时通常不使用） | `""` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `""` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "sms",
  "tenantId": "100000",
  "phonenumber": "13800138000",
  "smsCode": "567890"
}
```

---

*基于 `org.dromara.common.core.domain.model.SmsLoginBody` 源码生成 · 2026-07-14*
