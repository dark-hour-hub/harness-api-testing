# XcxLoginBody — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `XcxLoginBody` |
| **全限定名** | `org.dromara.common.core.domain.model.XcxLoginBody` |
| **类型** | 请求体 DTO |
| **所属模块** | 认证模块 (auth) |
| **父类** | `LoginBody` |
| **序列化特性** | 无特殊配置 |
| **说明** | 小程序登录请求体，用于微信/支付宝等小程序 code 换取 openid 方式登录 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| appid | `appid` | string | 否 | — | — | 小程序 appid（多个小程序时用于区分） | `"wx1234567890abcdef"` |
| xcxCode | `xcxCode` | string | ✅ | `@NotBlank(message="{xcx.code.not.blank}")` | — | 小程序登录凭证 code（由 wx.login 等接口获取） | `"081aBcDeFgHiJkLmN"` |

### 继承自 LoginBody 的字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| clientId | `clientId` | string | ✅ | `@NotBlank` | — | 客户端ID | `"e2f4c8a1"` |
| grantType | `grantType` | string | ✅ | `@NotBlank` | — | 授权类型，固定为 `"xcx"` | `"xcx"` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"100000"` |
| code | `code` | string | 否 | — | — | 验证码（小程序登录时通常不使用） | `""` |
| uuid | `uuid` | string | 否 | — | — | 唯一标识（验证码 Redis key） | `""` |

---

## JSON 示例

```json
{
  "clientId": "e2f4c8a1",
  "grantType": "xcx",
  "tenantId": "100000",
  "appid": "wx1234567890abcdef",
  "xcxCode": "081aBcDeFgHiJkLmN"
}
```

---

*基于 `org.dromara.common.core.domain.model.XcxLoginBody` 源码生成 · 2026-07-14*
