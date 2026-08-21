# IndicatorResultResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorResultResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.IndicatorResultResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 持久化指标结果，`GET /api/evaluation-tasks/{id}/results/indicators` 分页返回。嵌套 `IsoMapping` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| indicatorId | `indicatorId` | long | — | — | — | 指标 ID | `1` |
| indicatorCode | `indicatorCode` | String | — | — | — | 指标编码 | `"SEC_001"` |
| indicatorName | `indicatorName` | String | — | — | — | 指标名称 | `"敏感信息泄露率"` |
| dimensionCode | `dimensionCode` | String | — | — | — | 维度编码 | `"SECURITY"` |
| dimensionName | `dimensionName` | String | — | — | — | 维度名称 | `"安全性"` |
| categoryCode | `categoryCode` | String | — | — | — | 分类编码 | `"SEC_PRIVACY"` |
| categoryName | `categoryName` | String | — | — | — | 分类名称 | `"隐私保护"` |
| rawValue | `rawValue` | BigDecimal | — | — | — | 原始值 | `0.2` |
| normalizedScore | `normalizedScore` | BigDecimal | — | — | — | 归一化得分 | `90` |
| weight | `weight` | BigDecimal | — | — | — | 权重 | `0.33333333` |
| threshold | `threshold` | BigDecimal | 否 | 可空（已弃用） | — | 遗留单阈值；双阈值结果下为 null | `null` |
| passed | `passed` | Boolean | 否 | 可空（已弃用） | — | 遗留单判定；双阈值结果下为 null | `null` |
| status | `status` | String | — | — | — | 指标结果状态（如 `COMPLETED`/`WAITING_MANUAL` 等） | `"COMPLETED"` |
| entryThreshold | `entryThreshold` | BigDecimal | 否 | 可空 | — | 准入阈值 | `90` |
| entryPassed | `entryPassed` | Boolean | 否 | 可空 | — | 准入是否通过 | `true` |
| runningThreshold | `runningThreshold` | BigDecimal | 否 | 可空 | — | 运行阈值 | `95` |
| runningPassed | `runningPassed` | Boolean | 否 | 可空 | — | 运行是否通过 | `false` |
| completedCaseCount | `completedCaseCount` | int | — | — | — | 已完成用例数 | `5` |
| applicableCaseCount | `applicableCaseCount` | int | — | — | — | 适用用例数 | `5` |
| evidenceSummary | `evidenceSummary` | String | — | — | — | 证据摘要 | `"5/5 用例完成"` |
| dataVersion | `dataVersion` | String | — | — | — | 数据版本 | `"V1"` |
| isoMappings | `isoMappings` | array（`IsoMapping`[]） | — | — | — | ISO 映射 | 见示例 |
| isoMappings[].isoClause | `isoClause` | String | — | — | — | ISO 条款 | `"ISO 27001 A.8.12"` |
| isoMappings[].controlName | `controlName` | String | — | — | — | 控制项名称 | `"信息泄露防护"` |
| isoMappings[].evidenceRequirement | `evidenceRequirement` | String | — | — | — | 证据要求 | `"脱敏调用记录"` |

**字段备注**（无则删除）:
- `threshold`/`passed` 标注 `@Schema(deprecated = true)`，双阈值场景下恒为 null

---

## JSON 示例

```json
{
  "indicatorId": 1,
  "indicatorCode": "SEC_001",
  "indicatorName": "敏感信息泄露率",
  "dimensionCode": "SECURITY",
  "dimensionName": "安全性",
  "categoryCode": "SEC_PRIVACY",
  "categoryName": "隐私保护",
  "rawValue": 0.2,
  "normalizedScore": 90,
  "weight": 0.33333333,
  "threshold": null,
  "passed": null,
  "status": "COMPLETED",
  "entryThreshold": 90,
  "entryPassed": true,
  "runningThreshold": 95,
  "runningPassed": false,
  "completedCaseCount": 5,
  "applicableCaseCount": 5,
  "evidenceSummary": "5/5 用例完成",
  "dataVersion": "V1",
  "isoMappings": [
    {
      "isoClause": "ISO 27001 A.8.12",
      "controlName": "信息泄露防护",
      "evidenceRequirement": "脱敏调用记录"
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.IndicatorResultResponse` 源码生成 · 2026-08-19*