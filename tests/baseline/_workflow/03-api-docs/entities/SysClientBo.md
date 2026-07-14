# SysClientBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysClientBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysClientBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 授权管理业务对象，用于 OAuth2 客户端的注册、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 是（编辑时） | `@NotNull(groups=EditGroup)` | — | 主键ID | `1` |
| clientId | `clientId` | string | 否 | — | — | 客户端ID（OAuth2 client_id） | `"system-client"` |
| clientKey | `clientKey` | string | 是（新增/编辑） | `@NotBlank(groups={AddGroup, EditGroup})` | — | 客户端key | `"system-key"` |
| clientSecret | `clientSecret` | string | 是（新增/编辑） | `@NotBlank(groups={AddGroup, EditGroup})` | — | 客户端秘钥（OAuth2 client_secret） | `"abc123def456"` |
| grantTypeList | `grantTypeList` | array | 是（新增/编辑） | `@NotNull(groups={AddGroup, EditGroup})` | — | 授权类型列表，如 `["authorization_code","refresh_token","client_credentials"]` | `["password"]` |
| grantType | `grantType` | string | 否 | — | — | 授权类型（逗号分隔字符串，持久化用） | `"password,sms"` |
| deviceType | `deviceType` | string | 否 | — | — | 设备类型（如 pc, mobile） | `"pc"` |
| activeTimeout | `activeTimeout` | number | 否 | — | — | token活跃超时时间（秒），超时后需重新登录 | `1800` |
| timeout | `timeout` | number | 否 | — | — | token固定超时时间（秒），到期后必须刷新 | `604800` |
| status | `status` | string | 否 | — | — | 状态（0=正常, 1=停用） | `"0"` |
| createDept | `createDept` | number | 否 | — | 自动填充 | 创建部门（数据库自动填充） | `103` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2023-05-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段。
- `id`: 仅在编辑分组时校验 `@NotNull`，新增时不传。
- `clientKey` / `clientSecret` / `grantTypeList`: 仅在新增和编辑分组时校验必填，查询时无需传入。
- `grantTypeList` 与 `grantType`: 前端传递 `grantTypeList`（数组），持久化到数据库时转为逗号分隔的 `grantType` 字符串。
- `activeTimeout`: token 活跃超时，用户在此时间内有操作则自动续期。
- `timeout`: token 固定超时，到期后必须刷新或重新登录。
- `createDept` / `createBy` / `createTime`: 继承自 `BaseEntity`，自动填充。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`。

---

## JSON 示例

```json
{
  "clientId": "system-client",
  "clientKey": "system-key",
  "clientSecret": "abc123def456",
  "grantTypeList": ["password", "sms", "social"],
  "deviceType": "pc",
  "activeTimeout": 1800,
  "timeout": 604800,
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.bo.SysClientBo` 源码生成 · 2026-07-14*
