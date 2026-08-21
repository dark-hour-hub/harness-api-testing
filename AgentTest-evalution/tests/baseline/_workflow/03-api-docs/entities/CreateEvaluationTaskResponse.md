# CreateEvaluationTaskResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CreateEvaluationTaskResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateEvaluationTaskResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | ad-hoc 任务创建结果，`POST /api/evaluation-tasks/ad-hoc` 返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| taskNo | `taskNo` | String | — | — | — | 任务编号 | `"T20260819002"` |
| status | `status` | String（枚举 `TaskStatus`） | — | — | — | 任务状态：`CREATED`/`RUNNING`/`COMPLETED`/`FAILED` | `"CREATED"` |
| sourceType | `sourceType` | String（枚举 `TaskSourceType`） | — | — | — | 任务来源：`SCHEME`/`AD_HOC` | `"AD_HOC"` |
| sourceSchemeId | `sourceSchemeId` | Long | — | — | — | 来源方案 ID（ad-hoc 无方案时为 null） | `null` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "taskId": 1,
  "taskNo": "T20260819002",
  "status": "CREATED",
  "sourceType": "AD_HOC",
  "sourceSchemeId": null
}
```

---

*基于 `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateEvaluationTaskResponse` 源码生成 · 2026-08-19*
