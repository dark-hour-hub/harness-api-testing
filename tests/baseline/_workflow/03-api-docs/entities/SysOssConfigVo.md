# SysOssConfigVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysOssConfigVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysOssConfigVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | OSS 对象存储配置视图对象，用于配置列表和详情的查询响应 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| ossConfigId | `ossConfigId` | number | 否 | — | — | 配置主键 ID | `1` |
| configKey | `configKey` | string | 否 | — | — | 配置 key | `"minio"` |
| accessKey | `accessKey` | string | 否 | — | — | 访问密钥 accessKey | `"minioadmin"` |
| secretKey | `secretKey` | string | 否 | — | — | 访问密钥 secretKey | `"minioadmin"` |
| bucketName | `bucketName` | string | 否 | — | — | 桶名称 | `"ruoyi"` |
| prefix | `prefix` | string | 否 | — | — | 前缀（目录前缀） | `"dev/"` |
| endpoint | `endpoint` | string | 否 | — | — | 访问站点地址 | `"http://localhost:9000"` |
| domain | `domain` | string | 否 | — | — | 自定义域名 | `"https://oss.example.com"` |
| isHttps | `isHttps` | string | 否 | — | — | 是否 HTTPS（Y=是, N=否） | `"Y"` |
| status | `status` | string | 否 | — | — | 是否默认（0=是, 1=否） | `"0"` |
| region | `region` | string | 否 | — | — | 域（地域） | `"cn-north-1"` |
| ext1 | `ext1` | string | 否 | — | — | 扩展字段 | `""` |
| remark | `remark` | string | 否 | — | — | 备注 | `"MinIO 本地存储"` |
| accessPolicy | `accessPolicy` | string | 否 | — | — | 桶权限类型（0=private, 1=public, 2=custom） | `"1"` |

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
  "accessPolicy": "1"
}
```

---

*基于 `org.dromara.system.domain.vo.SysOssConfigVo` 源码生成 * 2026-07-14*
