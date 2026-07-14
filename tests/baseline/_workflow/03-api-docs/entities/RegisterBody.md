# RegisterBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `RegisterBody` |
| **全限定名** | `org.dromara.common.core.domain.model.RegisterBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户注册请求体，用于新用户自助注册账号 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| username | `username` | string | ✅ | `@NotBlank`, `@Length(min=2, max=30)` | — | 注册用户名 | `"newUser"` |
| password | `password` | string | ✅ | `@NotBlank`, `@Length(min=5, max=30)` | — | 注册密码（明文传输，后端 BCrypt 加密存储） | `"Pass@123"` |
| userType | `userType` | string | 否 | — | — | 用户类型（如 sys_user 等，由 `UserType` 枚举校验） | `"sys_user"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，注册场景值通常为 `"register"` 或自定义 | `"register"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 图形验证码（注册时用于人机验证） | `"1234"` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `"a1b2c3d4e5f6"` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "register",
  "tenantId": "100000",
  "username": "newUser",
  "password": "Pass@123",
  "userType": "sys_user",
  "code": "1234",
  "uuid": "a1b2c3d4e5f6"
}
```

---

*基于 `org.dromara.common.core.domain.model.RegisterBody` 源码生成 · 2026-07-14*
