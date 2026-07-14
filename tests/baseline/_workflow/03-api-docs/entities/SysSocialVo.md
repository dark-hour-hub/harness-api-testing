# SysSocialVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysSocialVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysSocialVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 社会化关系视图对象，用于展示第三方平台（如微信、QQ、微博等）授权绑定信息 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | — | — | 主键 ID | `1` |
| userId | `userId` | number | 否 | — | — | 系统用户 ID | `1` |
| tenantId | `tenantId` | string | 否 | — | — | 租户 ID | `"T0001"` |
| authId | `authId` | string | 否 | — | — | 第三方平台的唯一 ID | `"o7xXXXXX"` |
| source | `source` | string | 否 | — | — | 用户来源平台 | `"WECHAT_OPEN"` |
| accessToken | `accessToken` | string | 否 | — | — | 用户的授权令牌 | `"72_xxxxxxxxx"` |
| expireIn | `expireIn` | number | 否 | — | — | 授权令牌有效期（秒），部分平台可能没有 | `7200` |
| refreshToken | `refreshToken` | string | 否 | — | — | 刷新令牌，部分平台可能没有 | `"xx_yyyyyyy"` |
| openId | `openId` | string | 否 | — | — | 用户的 open id | `"oABCDEFG123456"` |
| userName | `userName` | string | 否 | — | — | 授权的第三方账号 | `"weixin_user"` |
| nickName | `nickName` | string | 否 | — | — | 授权的第三方昵称 | `"小明"` |
| email | `email` | string | 否 | — | — | 授权的第三方邮箱 | `"user@example.com"` |
| avatar | `avatar` | string | 否 | — | — | 授权的第三方头像地址 | `"https://thirdwx.qlogo.cn/xxx"` |
| accessCode | `accessCode` | string | 否 | — | — | 平台的授权信息 code，部分平台可能没有 | `"081xxxxx"` |
| unionId | `unionId` | string | 否 | — | — | 用户的 unionid | `"oLXXXXXXX"` |
| scope | `scope` | string | 否 | — | — | 授予的权限范围，部分平台可能没有 | `"snsapi_userinfo"` |
| tokenType | `tokenType` | string | 否 | — | — | 个别平台的授权信息（如 Bearer），部分平台可能没有 | `"Bearer"` |
| idToken | `idToken` | string | 否 | — | — | id token（OIDC），部分平台可能没有 | `"eyJhbGciOi..."` |
| macAlgorithm | `macAlgorithm` | string | 否 | — | — | 小米平台用户的附带属性（macAlgorithm），部分平台可能没有 | `"HmacSHA256"` |
| macKey | `macKey` | string | 否 | — | — | 小米平台用户的附带属性（macKey），部分平台可能没有 | `"xxxxx"` |
| code | `code` | string | 否 | — | — | 用户的授权 code，部分平台可能没有 | `"061xxxxx"` |
| oauthToken | `oauthToken` | string | 否 | — | — | Twitter 平台 oauthToken，部分平台可能没有 | `"xxxxx-xxxxx"` |
| oauthTokenSecret | `oauthTokenSecret` | string | 否 | — | — | Twitter 平台 oauthTokenSecret，部分平台可能没有 | `"yyyyyyy"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（绑定时间） | `"2026-07-01 10:00:00"` |

---

## JSON 示例

```json
{
  "id": 1,
  "userId": 1,
  "tenantId": "T0001",
  "authId": "o7xXXXXX",
  "source": "WECHAT_OPEN",
  "accessToken": "72_xxxxxxxxx",
  "expireIn": 7200,
  "refreshToken": "xx_yyyyyyy",
  "openId": "oABCDEFG123456",
  "userName": "weixin_user",
  "nickName": "小明",
  "email": "user@example.com",
  "avatar": "https://thirdwx.qlogo.cn/xxx",
  "accessCode": "081xxxxx",
  "unionId": "oLXXXXXXX",
  "scope": "snsapi_userinfo",
  "createTime": "2026-07-01 10:00:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysSocialVo` 源码生成 * 2026-07-14*
