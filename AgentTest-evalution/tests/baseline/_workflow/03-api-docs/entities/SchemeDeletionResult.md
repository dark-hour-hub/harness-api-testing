# SchemeDeletionResult — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SchemeDeletionResult` |
| **全限定名** | `com.czbank.aicgs.evaluation.scheme.application.SchemeDeletionResult` |
| **类型** | 响应体 VO |
| **所属模块** | 评测方案模块（scheme） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 方案删除结果（`DELETE /api/evaluation-schemes/{id}`）：未引用草稿物理删除，被引用已发布方案转归档 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| schemeId | `schemeId` | long | — | — | — | 方案 ID | `1` |
| originalStatus | `originalStatus` | String（枚举 `SchemeStatus`） | — | — | — | 删除前状态：`DRAFT`/`PUBLISHED`/`ARCHIVED` | `"PUBLISHED"` |
| action | `action` | String（枚举 `SchemeDeletionAction`） | — | — | — | 执行动作：`PHYSICALLY_DELETED`/`ARCHIVED` | `"ARCHIVED"` |
| taskReferenceCount | `taskReferenceCount` | long | — | — | — | 任务引用数 | `3` |
| reportReferenceCount | `reportReferenceCount` | long | — | — | — | 报告引用数 | `1` |
| resultingStatus | `resultingStatus` | String（枚举 `SchemeStatus`） | — | — | — | 删除后状态 | `"ARCHIVED"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "schemeId": 1,
  "originalStatus": "PUBLISHED",
  "action": "ARCHIVED",
  "taskReferenceCount": 3,
  "reportReferenceCount": 1,
  "resultingStatus": "ARCHIVED"
}
```

---

*基于 `com.czbank.aicgs.evaluation.scheme.application.SchemeDeletionResult` 源码生成 · 2026-08-19*