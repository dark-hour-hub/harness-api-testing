# SubmitMeasurementRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SubmitMeasurementRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.measurement.adapter.in.web.SubmitMeasurementRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 评测任务模块（task / measurement） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 提交指标测量值作为草稿证据（DRAFT 状态）。无校验注解，所有字段均可选（`POST /api/evaluation-tasks/{taskId}/measurements`） |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| indicatorId | `indicatorId` | long | 否 | — | — | 指标 ID | `1` |
| measurementType | `measurementType` | String | 否 | — | — | 测量类型 | `"LLM_JUDGE"` |
| rawValue | `rawValue` | BigDecimal | 否 | — | — | 原始测量值 | `0.2` |
| unit | `unit` | String | 否 | — | — | 单位 | `"%"` |
| measurementPayloadJson | `measurementPayloadJson` | String | 否 | — | — | 测量载荷 JSON | `"{\"sample\": 100}"` |
| sourceSystem | `sourceSystem` | String | 否 | — | — | 来源系统 | `"dify"` |
| sourceReference | `sourceReference` | String | 否 | — | — | 来源引用 | `"run-123"` |
| periodStart | `periodStart` | String（LocalDateTime） | 否 | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 统计周期开始 | `"2026-08-01T00:00:00+08:00"` |
| periodEnd | `periodEnd` | String（LocalDateTime） | 否 | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 统计周期结束 | `"2026-08-31T23:59:59+08:00"` |
| collectedAt | `collectedAt` | String（LocalDateTime） | 否 | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 采集时间 | `"2026-08-19T10:00:00+08:00"` |
| submittedBy | `submittedBy` | String | 否 | — | — | 提交人 | `"expert"` |
| remark | `remark` | String | 否 | — | — | 备注 | `"人工复核证据"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "indicatorId": 1,
  "measurementType": "LLM_JUDGE",
  "rawValue": 0.2,
  "unit": "%",
  "measurementPayloadJson": "{\"sample\": 100}",
  "sourceSystem": "dify",
  "sourceReference": "run-123",
  "periodStart": "2026-08-01T00:00:00+08:00",
  "periodEnd": "2026-08-31T23:59:59+08:00",
  "collectedAt": "2026-08-19T10:00:00+08:00",
  "submittedBy": "expert",
  "remark": "人工复核证据"
}
```

---

*基于 `com.czbank.aicgs.evaluation.measurement.adapter.in.web.SubmitMeasurementRequest` 源码生成 · 2026-08-19*
