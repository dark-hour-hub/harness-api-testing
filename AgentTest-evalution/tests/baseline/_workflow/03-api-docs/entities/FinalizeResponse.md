# FinalizeResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FinalizeResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationResultController.FinalizeResponse` |
| **类型** | 响应体 VO（嵌套 record，位于 `EvaluationResultController` 内） |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 显式重算评分结果，`POST /api/evaluation-tasks/{id}/finalize` 返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| finalized | `finalized` | boolean | — | — | — | 是否已重算完成 | `true` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "taskId": 1,
  "finalized": true
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationResultController.FinalizeResponse` 源码生成 · 2026-08-19*