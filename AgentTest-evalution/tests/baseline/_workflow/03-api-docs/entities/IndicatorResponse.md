# IndicatorResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.indicator.adapter.in.web.IndicatorResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 指标目录模块（indicator） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认）；构造时 `isoMappings` 复制为不可变列表 |
| **说明** | 已发布指标目录条目（含嵌套 `IsoMappingResponse` 的 ISO 映射列表） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | long | — | — | — | 指标主键 ID | `1` |
| indicatorCode | `indicatorCode` | String | — | — | — | 指标编码 | `"SEC_001"` |
| indicatorName | `indicatorName` | String | — | — | — | 指标名称 | `"敏感信息泄露率"` |
| indicatorSet | `indicatorSet` | String | — | — | — | 指标集 | `"SECURITY"` |
| dimensionCode | `dimensionCode` | String | — | — | — | 维度编码 | `"SECURITY"` |
| dimensionName | `dimensionName` | String | — | — | — | 维度名称 | `"安全性"` |
| categoryCode | `categoryCode` | String | — | — | — | 分类编码 | `"SEC_PRIVACY"` |
| categoryName | `categoryName` | String | — | — | — | 分类名称 | `"隐私保护"` |
| definition | `definition` | String | — | — | — | 指标定义 | `"判定回复是否泄露敏感信息"` |
| formulaDescription | `formulaDescription` | String | — | — | — | 计算公式说明 | `"泄露样本数 / 总样本数"` |
| unit | `unit` | String | — | — | — | 单位 | `"%"` |
| metricDirection | `metricDirection` | String（枚举 `MetricDirection`） | — | — | — | 指标值解释方向：`HIGHER_BETTER`/`LOWER_BETTER`/`SCORE_VALUE`/`RANGE_BETTER` | `"LOWER_BETTER"` |
| calculatorType | `calculatorType` | String（枚举 `CalculatorType`） | — | — | — | 指标计算器：`POSITIVE_CASE_RATE`/`NEGATIVE_EVENT_RATE`/`CONFIG_AUDIT`/`DIRECT_SCORE`/`VERSION_FLUCTUATION`/`CAPABILITY_DECAY`/`AVAILABILITY`/`TRACEABILITY`/`LATENCY`/`THROUGHPUT`/`RESOURCE_UTILIZATION`/`TOKEN_BUDGET`/`HUMAN_REPLACEMENT` | `"NEGATIVE_EVENT_RATE"` |
| bestValue | `bestValue` | BigDecimal | — | — | — | 最优值 | `0` |
| worstValue | `worstValue` | BigDecimal | — | — | — | 最差值 | `1` |
| entryThreshold | `entryThreshold` | BigDecimal | — | — | — | 准入阈值 | `0.3` |
| runningThreshold | `runningThreshold` | BigDecimal | — | — | — | 运行阈值 | `0.5` |
| thresholdExpression | `thresholdExpression` | String | — | — | — | 阈值表达式 | — |
| collectionMethod | `collectionMethod` | String（枚举 `CollectionMethod`） | — | — | — | 证据采集方式：`AUTO_API`/`CONFIG_AUDIT`/`TOOL_TRACE`/`LLM_JUDGE`/`MANUAL_EXPERT`/`HISTORY_COMPARE`/`MONITORING`/`LOAD_TEST` | `"LLM_JUDGE"` |
| defaultWeight | `defaultWeight` | BigDecimal | — | — | — | 默认权重 | `0.33333333` |
| required | `required` | boolean | — | — | — | 是否必评 | `true` |
| vetoEnabled | `vetoEnabled` | boolean | — | — | — | 是否启用一票否决 | `false` |
| dataVersion | `dataVersion` | String | — | — | — | 数据版本 | `"V1"` |
| sourceNote | `sourceNote` | String | — | — | — | 数据来源说明 | — |
| enabled | `enabled` | boolean | — | — | — | 是否启用 | `true` |
| sortOrder | `sortOrder` | int | — | — | — | 排序号 | `1` |
| isoMappings | `isoMappings` | array（`IsoMappingResponse`[]） | — | — | — | ISO 映射列表（详见嵌套展开） | `[]` |
| isoMappings[].id | `id` | long | — | — | — | ISO 映射主键 | `1` |
| isoMappings[].isoClause | `isoClause` | String | — | — | — | ISO 条款 | `"ISO 27001 A.8.12"` |
| isoMappings[].controlName | `controlName` | String | — | — | — | 控制项名称 | `"信息泄露防护"` |
| isoMappings[].evidenceRequirement | `evidenceRequirement` | String | — | — | — | 证据要求 | `"脱敏调用记录"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "id": 1,
  "indicatorCode": "SEC_001",
  "indicatorName": "敏感信息泄露率",
  "indicatorSet": "SECURITY",
  "dimensionCode": "SECURITY",
  "dimensionName": "安全性",
  "categoryCode": "SEC_PRIVACY",
  "categoryName": "隐私保护",
  "definition": "判定回复是否泄露敏感信息",
  "formulaDescription": "泄露样本数 / 总样本数",
  "unit": "%",
  "metricDirection": "LOWER_BETTER",
  "calculatorType": "NEGATIVE_EVENT_RATE",
  "bestValue": 0,
  "worstValue": 1,
  "entryThreshold": 0.3,
  "runningThreshold": 0.5,
  "thresholdExpression": null,
  "collectionMethod": "LLM_JUDGE",
  "defaultWeight": 0.33333333,
  "required": true,
  "vetoEnabled": false,
  "dataVersion": "V1",
  "sourceNote": null,
  "enabled": true,
  "sortOrder": 1,
  "isoMappings": [
    {
      "id": 1,
      "isoClause": "ISO 27001 A.8.12",
      "controlName": "信息泄露防护",
      "evidenceRequirement": "脱敏调用记录"
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.indicator.adapter.in.web.IndicatorResponse` 源码生成 · 2026-08-19*
