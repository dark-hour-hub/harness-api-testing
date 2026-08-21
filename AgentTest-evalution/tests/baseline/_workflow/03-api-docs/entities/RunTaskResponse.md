# RunTaskResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `RunTaskResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.execution.adapter.in.web.RunTaskResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / execution） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 任务启动结果（HTTP 202），`POST /api/evaluation-tasks/{id}/run` 返回，字段与 `EvaluationTaskProgress` 一致 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| status | `status` | String（枚举 `TaskStatus`） | — | — | — | 任务状态 | `"RUNNING"` |
| progress | `progress` | BigDecimal | — | — | — | 进度（0~1） | `0` |
| totalCount | `totalCount` | long | — | — | — | 总用例数 | `10` |
| completedCount | `completedCount` | long | — | — | — | 已完成数 | `0` |
| successCount | `successCount` | long | — | — | — | 成功数 | `0` |
| failureCount | `failureCount` | long | — | — | — | 失败数 | `0` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "taskId": 1,
  "status": "RUNNING",
  "progress": 0,
  "totalCount": 10,
  "completedCount": 0,
  "successCount": 0,
  "failureCount": 0
}
```

---

*基于 `com.czbank.aicgs.evaluation.execution.adapter.in.web.RunTaskResponse` 源码生成 · 2026-08-19*