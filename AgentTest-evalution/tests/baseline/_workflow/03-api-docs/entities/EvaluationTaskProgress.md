# EvaluationTaskProgress — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationTaskProgress` |
| **全限定名** | `com.czbank.aicgs.evaluation.task.application.query.EvaluationTaskProgress` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 任务持久化进度计数，`GET /api/evaluation-tasks/{id}/progress` 返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| status | `status` | String（枚举 `TaskStatus`） | — | — | — | 任务状态 | `"RUNNING"` |
| progress | `progress` | BigDecimal | — | — | — | 进度（0~1） | `0.5` |
| totalCount | `totalCount` | long | — | — | — | 总用例数 | `10` |
| completedCount | `completedCount` | long | — | — | — | 已完成数 | `5` |
| successCount | `successCount` | long | — | — | — | 成功数 | `4` |
| failureCount | `failureCount` | long | — | — | — | 失败数 | `1` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "taskId": 1,
  "status": "RUNNING",
  "progress": 0.5,
  "totalCount": 10,
  "completedCount": 5,
  "successCount": 4,
  "failureCount": 1
}
```

---

*基于 `com.czbank.aicgs.evaluation.task.application.query.EvaluationTaskProgress` 源码生成 · 2026-08-19*
