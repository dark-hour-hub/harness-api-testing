# SysOssUploadVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysOssUploadVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysOssUploadVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 文件上传响应视图对象，封装文件上传成功后的基本信息（URL、文件名、OSS ID） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| url | `url` | string | 否 | — | — | 文件访问 URL 地址 | `"https://oss.example.com/ruoyi/20260714_abc123.png"` |
| fileName | `fileName` | string | 否 | — | — | 文件名（存储后的文件名） | `"20260714_abc123.png"` |
| ossId | `ossId` | string | 否 | — | — | 对象存储主键 ID | `"1001"` |

**字段备注**:
- `ossId`: 类型为 `String`（与 SysOssVo 中的 Long 类型不同），用于前端回显

---

## JSON 示例

```json
{
  "url": "https://oss.example.com/ruoyi/20260714_abc123.png",
  "fileName": "20260714_abc123.png",
  "ossId": "1001"
}
```

---

*基于 `org.dromara.system.domain.vo.SysOssUploadVo` 源码生成 * 2026-07-14*
