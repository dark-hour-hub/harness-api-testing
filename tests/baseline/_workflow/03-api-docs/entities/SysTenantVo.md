# SysTenantVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysTenantVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysTenantVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 租户视图对象，用于租户列表和详情查询的响应数据 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | — | — | 租户 ID | `1` |
| tenantId | `tenantId` | string | 否 | — | — | 租户编号 | `"T0001"` |
| contactUserName | `contactUserName` | string | 否 | — | — | 联系人姓名 | `"张三"` |
| contactPhone | `contactPhone` | string | 否 | — | — | 联系电话 | `"13800138000"` |
| companyName | `companyName` | string | 否 | — | — | 企业名称 | `"示例科技有限公司"` |
| licenseNumber | `licenseNumber` | string | 否 | — | — | 统一社会信用代码 | `"91110000XXXXXXXXXX"` |
| address | `address` | string | 否 | — | — | 企业地址 | `"北京市朝阳区XX路XX号"` |
| domain | `domain` | string | 否 | — | — | 域名 | `"example.ruoyi.com"` |
| intro | `intro` | string | 否 | — | — | 企业简介 | `"专注于企业级软件开发"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"重要客户"` |
| packageId | `packageId` | number | 否 | — | — | 租户套餐编号 | `1` |
| expireTime | `expireTime` | string | 否 | — | — | 过期时间 | `"2026-12-31 23:59:59"` |
| accountCount | `accountCount` | number | 否 | — | — | 用户数量（-1 不限制） | `100` |
| status | `status` | string | 否 | — | — | 租户状态（0=正常 1=停用） | `"0"` |

---

## JSON 示例

```json
{
  "id": 1,
  "tenantId": "T0001",
  "contactUserName": "张三",
  "contactPhone": "13800138000",
  "companyName": "示例科技有限公司",
  "licenseNumber": "91110000XXXXXXXXXX",
  "address": "北京市朝阳区XX路XX号",
  "domain": "example.ruoyi.com",
  "intro": "专注于企业级软件开发",
  "remark": "重要客户",
  "packageId": 1,
  "expireTime": "2026-12-31 23:59:59",
  "accountCount": 100,
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.vo.SysTenantVo` 源码生成 * 2026-07-14*
