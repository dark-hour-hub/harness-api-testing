# EvaluationSchemeResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationSchemeResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.scheme.adapter.in.web.EvaluationSchemeResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测方案模块（scheme） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 持久化评测方案及生命周期状态（`GET/POST/PUT /api/evaluation-schemes`、publish/clone/archive 接口返回）。嵌套 `DimensionWeights`、`SchemeCategory`、`SchemeIndicator`、`SchemeTestCase` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Long | — | — | — | 方案 ID | `1` |
| schemeCode | `schemeCode` | String | — | — | — | 方案编码 | `"SCHEME_001"` |
| schemeName | `schemeName` | String | — | — | — | 方案名称 | `"年度评测方案"` |
| version | `version` | String | — | — | — | 版本号 | `"1.0.0"` |
| catalogVersion | `catalogVersion` | String | — | — | — | 目录版本 | `"V1"` |
| status | `status` | String（枚举 `SchemeStatus`） | — | — | — | 方案状态：`DRAFT`/`PUBLISHED`/`ARCHIVED` | `"PUBLISHED"` |
| evaluationMode | `evaluationMode` | String（枚举 `EvaluationMode`） | — | — | — | 评测模式：`COMPREHENSIVE`/`SPECIAL` | `"COMPREHENSIVE"` |
| evaluationType | `evaluationType` | String（枚举 `EvaluationType`） | 否 | —（已弃用） | — | 遗留评测类型 | `null` |
| riskTier | `riskTier` | String（枚举 `RiskTier`） | — | — | — | 风险等级 | `"B"` |
| thresholdLevel | `thresholdLevel` | String（枚举 `ThresholdLevel`） | 否 | —（已弃用） | — | 遗留阈值等级 | `null` |
| dimensionWeights | `dimensionWeights` | object（`DimensionWeights`） | — | — | — | 维度权重（JSON 键 `weights`） | 见示例 |
| safetyVetoEnabled | `safetyVetoEnabled` | boolean | — | — | — | 安全一票否决 | `true` |
| stopOnSafetyFailure | `stopOnSafetyFailure` | boolean | — | — | — | 安全失败停止 | `true` |
| scoringConfigJson | `scoringConfigJson` | String | — | — | — | 评分配置 JSON | `"{}"` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-08-01T10:00:00+08:00"` |
| updatedAt | `updatedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 更新时间 | `"2026-08-10T10:00:00+08:00"` |
| categories | `categories` | array（`SchemeCategory`[]） | — | — | — | 分类选择（字段同请求：id/categoryId/weightOverride/required/applicable） | 见示例 |
| indicators | `indicators` | array（`SchemeIndicator`[]） | — | — | — | 指标选择（字段同请求，含 notApplicableReason） | 见示例 |
| testCases | `testCases` | array（`SchemeTestCase`[]） | — | — | — | 用例选择（字段同请求：id/testCaseId/weightOverride/enabled） | 见示例 |

**字段备注**（无则删除）:
- `dimensionWeights` JSON 键为 `weights`（`@JsonProperty`），便捷方法 `safety()`/`capability()`/`evolution()` 为 `@JsonIgnore` 不序列化

---

## JSON 示例

```json
{
  "id": 1,
  "schemeCode": "SCHEME_001",
  "schemeName": "年度评测方案",
  "version": "1.0.0",
  "catalogVersion": "V1",
  "status": "PUBLISHED",
  "evaluationMode": "COMPREHENSIVE",
  "evaluationType": null,
  "riskTier": "B",
  "thresholdLevel": null,
  "dimensionWeights": {
    "weights": {
      "SAFETY": 0.4,
      "CAPABILITY": 0.35,
      "EVOLUTION": 0.25
    }
  },
  "safetyVetoEnabled": true,
  "stopOnSafetyFailure": true,
  "scoringConfigJson": "{}",
  "createdAt": "2026-08-01T10:00:00+08:00",
  "updatedAt": "2026-08-10T10:00:00+08:00",
  "categories": [
    {
      "id": 1,
      "categoryId": 1,
      "weightOverride": null,
      "required": false,
      "applicable": true
    }
  ],
  "indicators": [
    {
      "id": 1,
      "indicatorId": 1,
      "weightOverride": null,
      "thresholdOverride": null,
      "normalizationOverrideJson": null,
      "required": false,
      "applicable": true,
      "notApplicableReason": null
    }
  ],
  "testCases": [
    {
      "id": 1,
      "testCaseId": 1,
      "weightOverride": null,
      "enabled": true
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.scheme.adapter.in.web.EvaluationSchemeResponse` 源码生成 · 2026-08-19*