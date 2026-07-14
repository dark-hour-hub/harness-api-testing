# SysOssVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysOssVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysOssVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | OSS 对象存储视图对象，用于文件上传后的响应及文件列表查询 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| ossId | `ossId` | number | 否 | — | — | 对象存储主键 ID | `1001` |
| fileName | `fileName` | string | 否 | — | — | 文件名（存储后的文件名） | `"20260714_abc123.png"` |
| originalName | `originalName` | string | 否 | — | — | 原始文件名 | `"avatar.png"` |
| fileSuffix | `fileSuffix` | string | 否 | — | — | 文件后缀名 | `".png"` |
| url | `url` | string | 否 | — | — | 文件访问 URL 地址（私有桶为 120 秒临时签名 URL） | `"https://oss.example.com/ruoyi/20260714_abc123.png?sign=xxx"` |
| ext1 | `ext1` | string | 否 | — | — | 扩展字段（JSON 字符串，含文件大小 fileSize、contentType） | `"{\"fileSize\":102400,\"contentType\":\"image/png\"}"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（上传时间） | `"2026-07-14 15:30:00"` |
| createBy | `createBy` | number | 否 | — | — | 上传人 ID | `1` |
| createByName | `createByName` | string | 否 | — | — | 上传人名称（通过 @Translation 翻译 createBy） | `"张三"` |
| service | `service` | string | 否 | — | — | 服务商（OSS 配置 key） | `"minio"` |

**字段备注**:
- `createByName`: 通过 `@Translation(type = USER_ID_TO_NAME, mapper = "createBy")` 翻译获得，非数据库字段
- `url`: 若桶权限为 private，URL 会被替换为 120 秒有效期的临时签名 URL

---

## JSON 示例

```json
{
  "ossId": 1001,
  "fileName": "20260714_abc123.png",
  "originalName": "avatar.png",
  "fileSuffix": ".png",
  "url": "https://oss.example.com/ruoyi/20260714_abc123.png?sign=xxx",
  "ext1": "{\"fileSize\":102400,\"contentType\":\"image/png\"}",
  "createTime": "2026-07-14 15:30:00",
  "createBy": 1,
  "createByName": "张三",
  "service": "minio"
}
```

---

*基于 `org.dromara.system.domain.vo.SysOssVo` 源码生成 * 2026-07-14*
