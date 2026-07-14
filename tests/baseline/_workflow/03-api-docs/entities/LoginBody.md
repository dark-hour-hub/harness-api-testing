# LoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `LoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.LoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户登录请求体基类，所有登录方式（密码、短信、邮箱、小程序、三方登录、注册）均继承此类 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank(message="{auth.clientid.not.blank}")` | — | 客户端ID，用于区分不同的客户端应用 | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank(message="{auth.grant.type.not.blank}")` | — | 授权类型（如 password、sms、email、xcx、social） | `"password"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID，多租户场景下标识所属租户 | `"100000"` |
| code | `code` | string | 否 | — | — | 验证码（图形验证码或短信/邮箱验证码） | `"1234"` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识，关联 Redis 中的验证码缓存 key | `"a1b2c3d4e5f6"` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "password",
  "tenantId": "100000",
  "code": "1234",
  "uuid": "a1b2c3d4e5f6"
}
```

---

*基于 `org.dromara.common.core.domain.model.LoginBody` 源码生成 · 2026-07-14*
