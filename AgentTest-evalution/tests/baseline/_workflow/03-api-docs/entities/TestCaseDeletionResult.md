# TestCaseDeletionResult — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `TestCaseDeletionResult` |
| **全限定名** | `com.czbank.aicgs.evaluation.testcase.application.service.TestCaseDeletionResult` |
| **类型** | 响应体 VO |
| **所属模块** | 测试用例模块（testcase） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 测试用例软删除结果，`DELETE /api/test-cases/{id}` 返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| testCaseId | `testCaseId` | long | — | — | — | 被删除的用例 ID | `1` |
| action | `action` | String | — | — | — | 删除动作（软删除标记，如 `"DELETED"`/`"SOFT_DELETED"`） | `"DELETED"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "testCaseId": 1,
  "action": "DELETED"
}
```

---

*基于 `com.czbank.aicgs.evaluation.testcase.application.service.TestCaseDeletionResult` 源码生成 · 2026-08-19*
