# SysTenantBo -- 业务对象 BO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysTenantBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysTenantBo` |
| **类型** | 业务对象 BO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（父类 `params` 字段为非空时包含） |
| **说明** | 租户业务对象，用于新增和编辑租户的请求参数封装 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | ✅ | `@NotNull`（EditGroup） | — | 租户主键 ID | `1` |
| tenantId | `tenantId` | string | 否 | — | — | 租户编号 | `"T0001"` |
| contactUserName | `contactUserName` | string | ✅ | `@NotBlank`（AddGroup, EditGroup） | — | 联系人姓名 | `"张三"` |
| contactPhone | `contactPhone` | string | ✅ | `@NotBlank`（AddGroup, EditGroup） | — | 联系电话 | `"13800138000"` |
| companyName | `companyName` | string | ✅ | `@NotBlank`（AddGroup, EditGroup） | — | 企业名称 | `"示例科技有限公司"` |
| username | `username` | string | ✅ | `@NotBlank`（AddGroup） | — | 创建系统用户的用户名 | `"admin_t0001"` |
| password | `password` | string | ✅ | `@NotBlank`（AddGroup） | — | 创建系统用户的密码 | `"Abc@1234"` |
| licenseNumber | `licenseNumber` | string | 否 | — | — | 统一社会信用代码 | `"91110000XXXXXXXXXX"` |
| address | `address` | string | 否 | — | — | 企业地址 | `"北京市朝阳区XX路XX号"` |
| domain | `domain` | string | 否 | — | — | 域名 | `"example.ruoyi.com"` |
| intro | `intro` | string | 否 | — | — | 企业简介 | `"专注于企业级软件开发"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"重要客户"` |
| packageId | `packageId` | number | ✅ | `@NotNull`（AddGroup） | — | 租户套餐编号 | `1` |
| expireTime | `expireTime` | string | 否 | — | — | 过期时间 | `"2026-12-31 23:59:59"` |
| accountCount | `accountCount` | number | 否 | — | — | 用户数量（-1 不限制） | `100` |
| status | `status` | string | 否 | — | — | 租户状态（0=正常 1=停用） | `"0"` |
| createDept | `createDept` | number | 否 | — | — | 创建部门（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | — | — | 创建者（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（继承自 BaseEntity） | `"2026-07-01 10:00:00"` |
| updateBy | `updateBy` | number | 否 | — | — | 更新者（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | — | — | 更新时间（继承自 BaseEntity） | `"2026-07-14 15:30:00"` |
| params | `params` | object | 否 | — | — | 请求参数（继承自 BaseEntity，非空序列化） | `{"key": "value"}` |

**字段备注**:
- `searchValue`: 搜索值（继承自 BaseEntity），`@JsonIgnore` 不参与序列化
- `username` / `password`: 仅在新增场景（AddGroup）时必填

---

## JSON 示例

```json
{
  "id": 1,
  "tenantId": "T0001",
  "contactUserName": "张三",
  "contactPhone": "13800138000",
  "companyName": "示例科技有限公司",
  "username": "admin_t0001",
  "password": "Abc@1234",
  "licenseNumber": "91110000XXXXXXXXXX",
  "address": "北京市朝阳区XX路XX号",
  "domain": "example.ruoyi.com",
  "intro": "专注于企业级软件开发",
  "remark": "重要客户",
  "packageId": 1,
  "expireTime": "2026-12-31 23:59:59",
  "accountCount": 100,
  "status": "0",
  "createDept": 103,
  "createBy": 1,
  "createTime": "2026-07-01 10:00:00",
  "updateBy": 1,
  "updateTime": "2026-07-14 15:30:00",
  "params": {}
}
```

---

*基于 `org.dromara.system.domain.bo.SysTenantBo` 源码生成 * 2026-07-14*
