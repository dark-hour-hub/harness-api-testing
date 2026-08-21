# SchemeValidationResult — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SchemeValidationResult` |
| **全限定名** | `com.czbank.aicgs.evaluation.scheme.application.SchemeValidationResult` |
| **类型** | 响应体 VO |
| **所属模块** | 评测方案模块（scheme） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 方案草稿校验结果（`POST /api/evaluation-schemes/{id}/validate`）。校验失败时响应 code=`SCHEME_400_INVALID` + 错误列表。`valid()` 为方法，不参与序列化 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| errors | `errors` | array（`ValidationError`[]） | — | — | — | 校验错误列表（空数组 = 校验通过） | 见示例 |
| errors[].field | `field` | String | — | — | — | 出错字段 | `"version"` |
| errors[].errorCode | `errorCode` | String | — | — | — | 错误码 | `"SCHEME_400_INVALID"` |
| errors[].message | `message` | String | — | — | — | 错误信息 | `"version must be numeric"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "errors": [
    {
      "field": "version",
      "errorCode": "SCHEME_400_INVALID",
      "message": "version must be numeric"
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.scheme.application.SchemeValidationResult` 源码生成 · 2026-08-19*