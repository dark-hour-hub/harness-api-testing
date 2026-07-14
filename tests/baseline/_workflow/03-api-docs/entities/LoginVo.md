# LoginVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `LoginVo` |
| **全限定名** | `org.dromara.web.domain.vo.LoginVo` |
| **类型** | 响应体 VO |
| **所属模块** | 认证模块 (auth) |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 登录验证信息响应体，登录成功后返回令牌及相关信息 |

---

## 注解转义说明

> 以下字段的 Java 字段名与 JSON 键名不一致，由 `@JsonProperty` 注解转换。

| Java 字段名 | JSON 键名 | 显示名 | 转义来源 |
|------------|----------|--------|----------|
| `accessToken` | `access_token` | 授权令牌 | `@JsonProperty("access_token")` |
| `refreshToken` | `refresh_token` | 刷新令牌 | `@JsonProperty("refresh_token")` |
| `expireIn` | `expire_in` | 令牌有效期 | `@JsonProperty("expire_in")` |
| `refreshExpireIn` | `refresh_expire_in` | 刷新令牌有效期 | `@JsonProperty("refresh_expire_in")` |
| `clientId` | `client_id` | 应用ID | `@JsonProperty("client_id")` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| accessToken | `access_token` | string | — | — | — | 授权令牌（JWT / Sa-Token），用于后续接口认证 | `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"` |
| refreshToken | `refresh_token` | string | — | — | — | 刷新令牌，用于 access_token 过期后刷新获取新令牌 | `"r1e2f3r4-e5s6-h7t8-o9k0-en1234567890"` |
| expireIn | `expire_in` | number | — | — | — | access_token 有效期（秒），由 Sa-Token 配置决定 | `7200` |
| refreshExpireIn | `refresh_expire_in` | number | — | — | — | refresh_token 有效期（秒） | `604800` |
| clientId | `client_id` | string | — | — | — | 客户端应用ID | `"e2f4c8a1"` |
| scope | `scope` | string | — | — | — | 令牌权限范围 | `"server"` |
| openid | `openid` | string | — | — | — | 用户 openid（三方登录时返回，如微信小程序） | `"oABC1234567890XYZ"` |

---

## JSON 示例

```json
{
  "access_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "refresh_token": "r1e2f3r4-e5s6-h7t8-o9k0-en1234567890",
  "expire_in": 7200,
  "refresh_expire_in": 604800,
  "client_id": "e2f4c8a1",
  "scope": "server",
  "openid": "oABC1234567890XYZ"
}
```

---

*基于 `org.dromara.web.domain.vo.LoginVo` 源码生成 · 2026-07-14*
