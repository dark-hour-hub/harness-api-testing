# SysClientVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysClientVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysClientVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 授权管理视图对象，用于 OAuth2 客户端列表查询、详情查看等接口的响应数据封装；支持 Excel 导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | — | — | — | 主键ID | `1` |
| clientId | `clientId` | string | — | — | — | 客户端ID（OAuth2 client_id） | `"system-client"` |
| clientKey | `clientKey` | string | — | — | — | 客户端key | `"system-key"` |
| clientSecret | `clientSecret` | string | — | — | — | 客户端秘钥（OAuth2 client_secret） | `"abc123def456"` |
| grantTypeList | `grantTypeList` | array | — | — | — | 授权类型列表，如 `["authorization_code", "password", "refresh_token"]` | `["password","sms"]` |
| grantType | `grantType` | string | — | — | — | 授权类型（逗号分隔字符串，持久化用） | `"password,sms,social"` |
| deviceType | `deviceType` | string | — | — | — | 设备类型（如 pc, app, mini） | `"pc"` |
| activeTimeout | `activeTimeout` | number | — | — | — | token活跃超时时间（秒） | `1800` |
| timeout | `timeout` | number | — | — | — | token固定超时时间（秒） | `604800` |
| status | `status` | string | — | — | — | 状态（0=正常, 1=停用） | `"0"` |

**字段备注**:
- `clientSecret`: 敏感信息，实际响应中可能经过脱敏处理（如部分字符替换为 `*`）。
- `grantTypeList` 与 `grantType`: `grantTypeList` 为前端友好的数组格式，`grantType` 为数据库持久化的逗号分隔字符串。
- `activeTimeout`: token 活跃超时时间，单位为秒。1800 秒 = 30 分钟。在此时间内用户有操作则 token 自动续期。
- `timeout`: token 固定超时时间，单位为秒。604800 秒 = 7 天。到期后必须刷新或重新登录。
- `status`: 0=正常（客户端可正常认证），1=停用（客户端被禁用，无法获取 token）。

---

## JSON 示例

```json
{
  "id": 1,
  "clientId": "system-client",
  "clientKey": "system-key",
  "clientSecret": "abc****f456",
  "grantTypeList": ["password", "sms", "social"],
  "grantType": "password,sms,social",
  "deviceType": "pc",
  "activeTimeout": 1800,
  "timeout": 604800,
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.vo.SysClientVo` 源码生成 · 2026-07-14*
