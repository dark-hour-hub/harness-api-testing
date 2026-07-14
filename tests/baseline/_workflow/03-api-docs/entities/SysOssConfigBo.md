# SysOssConfigBo -- 业务对象 BO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysOssConfigBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysOssConfigBo` |
| **类型** | 业务对象 BO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（父类 `params` 字段为非空时包含） |
| **说明** | 对象存储配置业务对象，用于 OSS 配置的新增和编辑操作 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| ossConfigId | `ossConfigId` | number | ✅ | `@NotNull`（EditGroup） | — | 配置主键 ID | `1` |
| configKey | `configKey` | string | ✅ | `@NotBlank`（AddGroup, EditGroup），`@Size`(2-100) | — | 配置 key | `"minio"` |
| accessKey | `accessKey` | string | ✅ | `@NotBlank`（AddGroup, EditGroup），`@Size`(2-100) | — | 访问密钥 accessKey | `"minioadmin"` |
| secretKey | `secretKey` | string | ✅ | `@NotBlank`（AddGroup, EditGroup），`@Size`(2-100) | — | 访问密钥 secretKey | `"minioadmin"` |
| bucketName | `bucketName` | string | ✅ | `@NotBlank`（AddGroup, EditGroup），`@Size`(2-100) | — | 桶名称 | `"ruoyi"` |
| prefix | `prefix` | string | 否 | — | — | 前缀（目录前缀） | `"dev/"` |
| endpoint | `endpoint` | string | ✅ | `@NotBlank`（AddGroup, EditGroup），`@Size`(2-100) | — | 访问站点 | `"http://localhost:9000"` |
| domain | `domain` | string | 否 | — | — | 自定义域名 | `"https://oss.example.com"` |
| isHttps | `isHttps` | string | 否 | — | — | 是否 HTTPS（Y=是, N=否） | `"Y"` |
| status | `status` | string | 否 | — | — | 是否默认（0=是, 1=否） | `"0"` |
| region | `region` | string | 否 | — | — | 域（地域） | `"cn-north-1"` |
| ext1 | `ext1` | string | 否 | — | — | 扩展字段 | `""` |
| remark | `remark` | string | 否 | — | — | 备注 | `"MinIO 本地存储"` |
| accessPolicy | `accessPolicy` | string | ✅ | `@NotBlank`（AddGroup, EditGroup） | — | 桶权限类型（0=private, 1=public, 2=custom） | `"1"` |
| createDept | `createDept` | number | 否 | — | — | 创建部门（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | — | — | 创建者（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（继承自 BaseEntity） | `"2026-07-01 10:00:00"` |
| updateBy | `updateBy` | number | 否 | — | — | 更新者（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | — | — | 更新时间（继承自 BaseEntity） | `"2026-07-14 15:30:00"` |
| params | `params` | object | 否 | — | — | 请求参数（继承自 BaseEntity，非空序列化） | `{}` |

**字段备注**:
- `searchValue`: 搜索值（继承自 BaseEntity），`@JsonIgnore` 不参与序列化
- `accessPolicy`: 枚举值 — `"0"` (private), `"1"` (public), `"2"` (custom)

---

## JSON 示例

```json
{
  "ossConfigId": 1,
  "configKey": "minio",
  "accessKey": "minioadmin",
  "secretKey": "minioadmin",
  "bucketName": "ruoyi",
  "prefix": "dev/",
  "endpoint": "http://localhost:9000",
  "domain": "https://oss.example.com",
  "isHttps": "Y",
  "status": "0",
  "region": "cn-north-1",
  "ext1": "",
  "remark": "MinIO 本地存储",
  "accessPolicy": "1",
  "createDept": 103,
  "createBy": 1,
  "createTime": "2026-07-01 10:00:00",
  "updateBy": 1,
  "updateTime": "2026-07-14 15:30:00",
  "params": {}
}
```

---

*基于 `org.dromara.system.domain.bo.SysOssConfigBo` 源码生成 * 2026-07-14*
