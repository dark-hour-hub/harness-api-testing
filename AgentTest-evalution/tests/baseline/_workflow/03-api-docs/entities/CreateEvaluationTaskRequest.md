# CreateEvaluationTaskRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CreateEvaluationTaskRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateEvaluationTaskRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 评测任务模块（task） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 快照 Agent + 已发布方案创建 CREATED 状态任务（`POST /api/evaluation-tasks`），`@Valid` 校验 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| agentId | `agentId` | Long | ✅ | `@NotNull` `@Positive` | — | 正向 Agent ID | `1` |
| schemeId | `schemeId` | Long | ✅ | `@NotNull` `@Positive` | — | 正向已发布方案 ID | `1` |
| createdBy | `createdBy` | String | 否 | `@Size(max=100)` | `"api"` | 创建人标签，最多 100 字符 | `"api"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "agentId": 1,
  "schemeId": 1,
  "createdBy": "api"
}
```

---

*基于 `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateEvaluationTaskRequest` 源码生成 · 2026-08-19*
