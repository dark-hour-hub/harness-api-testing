# ImportError — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `ImportError` |
| **全限定名** | `com.czbank.aicgs.evaluation.testcase.application.service.ImportTestCasesResult.ImportError` |
| **类型** | 响应体 VO（嵌套 record，位于 `ImportTestCasesResult` 内） |
| **所属模块** | 测试用例模块（testcase） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 批量/Excel 导入测试用例时的行级错误条目；错误响应体为 `ApiResponse<List<ImportError>>` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| rowIndex | `rowIndex` | int | — | — | — | 出错行号（JSON 数组从 1 计数；Excel 为物理行号） | `3` |
| field | `field` | String | — | — | — | 出错字段路径 | `"weight"` |
| errorCode | `errorCode` | String | — | — | — | 错误码（如 `COMMON_400_VALIDATION`/`COMMON_409_CONFLICT`/`TEST_CASE_400_RULE`） | `"COMMON_400_VALIDATION"` |
| message | `message` | String | — | — | — | 错误信息 | `"weight must be greater than 0"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "rowIndex": 3,
  "field": "weight",
  "errorCode": "COMMON_400_VALIDATION",
  "message": "weight must be greater than 0"
}
```

---

*基于 `com.czbank.aicgs.evaluation.testcase.application.service.ImportTestCasesResult.ImportError` 源码生成 · 2026-08-19*
