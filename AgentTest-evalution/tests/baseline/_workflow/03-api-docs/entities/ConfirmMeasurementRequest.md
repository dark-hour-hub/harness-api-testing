# ConfirmMeasurementRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `ConfirmMeasurementRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.measurement.adapter.in.web.ConfirmMeasurementRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 评测任务模块（task / measurement） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 确认草稿测量证据（DRAFT→CONFIRMED，`POST /api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm`） |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| confirmedBy | `confirmedBy` | String | 否 | — | — | 确认人 | `"expert"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "confirmedBy": "expert"
}
```

---

*基于 `com.czbank.aicgs.evaluation.measurement.adapter.in.web.ConfirmMeasurementRequest` 源码生成 · 2026-08-19*
