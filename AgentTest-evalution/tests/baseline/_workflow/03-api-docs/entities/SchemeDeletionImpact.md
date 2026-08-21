# SchemeDeletionImpact — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SchemeDeletionImpact` |
| **全限定名** | `com.czbank.aicgs.evaluation.scheme.application.SchemeDeletionImpact` |
| **类型** | 响应体 VO |
| **所属模块** | 评测方案模块（scheme） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 方案删除事务性影响预览（不执行删除），`GET /api/evaluation-schemes/{id}/deletion-impact` 返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| schemeId | `schemeId` | long | — | — | — | 方案 ID | `1` |
| status | `status` | String（枚举 `SchemeStatus`） | — | — | — | 当前状态：`DRAFT`/`PUBLISHED`/`ARCHIVED` | `"PUBLISHED"` |
| taskReferenceCount | `taskReferenceCount` | long | — | — | — | 任务引用数 | `3` |
| reportReferenceCount | `reportReferenceCount` | long | — | — | — | 报告引用数 | `1` |
| actionIfConfirmed | `actionIfConfirmed` | String（枚举 `SchemeDeletionAction`） | — | — | — | 若确认删除将执行的动作：`PHYSICALLY_DELETED`/`ARCHIVED` | `"ARCHIVED"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "schemeId": 1,
  "status": "PUBLISHED",
  "taskReferenceCount": 3,
  "reportReferenceCount": 1,
  "actionIfConfirmed": "ARCHIVED"
}
```

---

*基于 `com.czbank.aicgs.evaluation.scheme.application.SchemeDeletionImpact` 源码生成 · 2026-08-19*