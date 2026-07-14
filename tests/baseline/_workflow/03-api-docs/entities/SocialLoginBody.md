# SocialLoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SocialLoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.SocialLoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 三方社交登录请求体，用于第三方平台（如 Github、Gitee、微信开放平台等）OAuth 授权码登录，也用于前端回调绑定第三方账号 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| source | `source` | string | ✅ | `@NotBlank(message="{social.source.not.blank}")` | — | 第三方登录平台标识（如 github、gitee、wechat_open） | `"github"` |
| socialCode | `socialCode` | string | ✅ | `@NotBlank(message="{social.code.not.blank}")` | — | 第三方平台返回的授权 code | `"a1b2c3d4e5f6"` |
| socialState | `socialState` | string | ✅ | `@NotBlank(message="{social.state.not.blank}")` | — | 第三方登录 state 参数，用于防 CSRF 攻击 | `"state_abc123"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，固定为 `"social"` | `"social"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 验证码（三方登录时通常不使用） | `""` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `""` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "social",
  "tenantId": "100000",
  "source": "github",
  "socialCode": "a1b2c3d4e5f6",
  "socialState": "state_abc123"
}
```

---

*基于 `org.dromara.common.core.domain.model.SocialLoginBody` 源码生成 · 2026-07-14*
