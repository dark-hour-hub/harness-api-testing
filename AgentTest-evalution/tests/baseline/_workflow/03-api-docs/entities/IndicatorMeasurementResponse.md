# IndicatorMeasurementResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorMeasurementResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.measurement.adapter.in.web.IndicatorMeasurementResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / measurement） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 指标测量证据（草稿提交与确认接口返回），`POST /api/evaluation-tasks/{taskId}/measurements` 及 confirm 接口返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Long | — | — | — | 测量记录 ID | `1` |
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| indicatorId | `indicatorId` | long | — | — | — | 指标 ID | `1` |
| measurementType | `measurementType` | String | — | — | — | 测量类型 | `"LLM_JUDGE"` |
| status | `status` | String（枚举 `MeasurementStatus`） | — | — | — | 测量状态：`DRAFT`/`CONFIRMED`/`REJECTED` | `"DRAFT"` |
| rawValue | `rawValue` | BigDecimal | — | — | — | 原始测量值 | `0.2` |
| unit | `unit` | String | — | — | — | 单位 | `"%"` |
| measurementPayloadJson | `measurementPayloadJson` | String | — | — | — | 测量载荷 JSON | `"{\"sample\": 100}"` |
| sourceSystem | `sourceSystem` | String | — | — | — | 来源系统 | `"dify"` |
| sourceReference | `sourceReference` | String | — | — | — | 来源引用 | `"run-123"` |
| periodStart | `periodStart` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 周期开始 | `"2026-08-01T00:00:00+08:00"` |
| periodEnd | `periodEnd` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 周期结束 | `"2026-08-31T23:59:59+08:00"` |
| collectedAt | `collectedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 采集时间 | `"2026-08-19T10:00:00+08:00"` |
| submittedBy | `submittedBy` | String | — | — | — | 提交人 | `"expert"` |
| confirmedBy | `confirmedBy` | String | — | — | — | 确认人（未确认时 null） | `null` |
| confirmedAt | `confirmedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 确认时间 | `null` |
| remark | `remark` | String | — | — | — | 备注 | `"人工复核证据"` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-08-19T10:00:00+08:00"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "id": 1,
  "taskId": 1,
  "indicatorId": 1,
  "measurementType": "LLM_JUDGE",
  "status": "DRAFT",
  "rawValue": 0.2,
  "unit": "%",
  "measurementPayloadJson": "{\"sample\": 100}",
  "sourceSystem": "dify",
  "sourceReference": "run-123",
  "periodStart": "2026-08-01T00:00:00+08:00",
  "periodEnd": "2026-08-31T23:59:59+08:00",
  "collectedAt": "2026-08-19T10:00:00+08:00",
  "submittedBy": "expert",
  "confirmedBy": null,
  "confirmedAt": null,
  "remark": "人工复核证据",
  "createdAt": "2026-08-19T10:00:00+08:00"
}
```

---

*基于 `com.czbank.aicgs.evaluation.measurement.adapter.in.web.IndicatorMeasurementResponse` 源码生成 · 2026-08-19*