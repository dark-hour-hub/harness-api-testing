# EvaluationSchemeRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationSchemeRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.scheme.adapter.in.web.EvaluationSchemeRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 评测方案模块（scheme） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 评测方案草稿输入（`POST`/`PUT /api/evaluation-schemes`）。`@Valid` 校验。嵌套 `DimensionWeights`、`SchemeCategory`、`SchemeIndicator`、`SchemeTestCase` |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| schemeCode | `schemeCode` | String | ✅ | `@NotBlank` | — | 唯一方案编码 | `"SCHEME_001"` |
| schemeName | `schemeName` | String | ✅ | `@NotBlank` | — | 方案名称 | `"年度评测方案"` |
| version | `version` | String | ✅ | `@NotBlank` `@Size(max=64)` `@Pattern(SchemeValidator.VERSION_PATTERN)`（数字点分版本，message="version must be numeric"） | — | 版本号 | `"1.0.0"` |
| catalogVersion | `catalogVersion` | String | 否 | — | — | 指标目录版本，省略使用唯一默认版本 | `"V1"` |
| evaluationMode | `evaluationMode` | String（枚举 `EvaluationMode`） | ✅ | `@NotNull` | — | 评测覆盖模式：`COMPREHENSIVE`/`SPECIAL` | `"COMPREHENSIVE"` |
| evaluationType | `evaluationType` | String（枚举 `EvaluationType`） | 否 | —（已弃用） | — | 遗留生命周期类型，不再选择评分阈值 | `null` |
| riskTier | `riskTier` | String（枚举 `RiskTier`） | ✅ | `@NotNull` | — | 适用风险等级：`A`/`B`/`C`/`D` | `"B"` |
| thresholdLevel | `thresholdLevel` | String（枚举 `ThresholdLevel`） | 否 | —（已弃用） | — | 遗留单阈值选择 | `null` |
| dimensionWeights | `dimensionWeights` | object（`DimensionWeights`） | 否 | — | — | 可选维度权重（JSON 键 `weights`） | 见示例 |
| safetyVetoEnabled | `safetyVetoEnabled` | Boolean | 否 | — | `true` | 启用安全一票否决 | `true` |
| stopOnSafetyFailure | `stopOnSafetyFailure` | Boolean | 否 | — | `true` | 安全失败即停止 | `true` |
| scoringConfigJson | `scoringConfigJson` | String | 否 | — | — | 评分配置 JSON | `"{}"` |
| categories | `categories` | array（`SchemeCategory`[]） | 否 | — | — | 分类选择（详见嵌套展开） | 见示例 |
| categories[].id | `id` | Long | 否 | — | — | 记录 ID（新建时 null） | `null` |
| categories[].categoryId | `categoryId` | long | — | — | — | 目录分类 ID | `1` |
| categories[].weightOverride | `weightOverride` | BigDecimal | 否 | — | — | 权重覆盖 | `null` |
| categories[].required | `required` | boolean | — | — | — | 是否必评 | `false` |
| categories[].applicable | `applicable` | boolean | — | — | — | 是否适用 | `true` |
| indicators | `indicators` | array（`SchemeIndicator`[]） | 否 | — | — | 指标选择（详见嵌套展开） | 见示例 |
| indicators[].id | `id` | Long | 否 | — | — | 记录 ID（新建时 null） | `null` |
| indicators[].indicatorId | `indicatorId` | long | — | — | — | 目录指标 ID | `1` |
| indicators[].weightOverride | `weightOverride` | BigDecimal | 否 | — | — | 权重覆盖 | `null` |
| indicators[].thresholdOverride | `thresholdOverride` | BigDecimal | 否 | —（已弃用） | — | 遗留归一化锚点覆盖；不覆盖双判定 | `null` |
| indicators[].normalizationOverrideJson | `normalizationOverrideJson` | String | 否 | — | — | 归一化覆盖 JSON | `null` |
| indicators[].required | `required` | boolean | — | — | — | 是否必评 | `false` |
| indicators[].applicable | `applicable` | boolean | — | — | — | 是否适用 | `true` |
| indicators[].notApplicableReason | `notApplicableReason` | String | 否 | — | — | 不适用原因 | `null` |
| testCases | `testCases` | array（`SchemeTestCase`[]） | 否 | — | — | 用例选择（详见嵌套展开） | 见示例 |
| testCases[].id | `id` | Long | 否 | — | — | 记录 ID（新建时 null） | `null` |
| testCases[].testCaseId | `testCaseId` | long | — | — | — | 用例 ID | `1` |
| testCases[].weightOverride | `weightOverride` | BigDecimal | 否 | — | — | 权重覆盖 | `null` |
| testCases[].enabled | `enabled` | boolean | — | — | — | 是否启用 | `true` |

**字段备注**（无则删除）:
- `dimensionWeights` 为自定义类 `DimensionWeights`，序列化 JSON 键为 `weights`（`@JsonProperty`），未序列化 `safety()`/`capability()`/`evolution()` 便捷方法（`@JsonIgnore`）
- 存在兼容构造函数（无 `catalogVersion` 参数），反序列化时按 JSON 字段解析

---

## JSON 示例

```json
{
  "schemeCode": "SCHEME_001",
  "schemeName": "年度评测方案",
  "version": "1.0.0",
  "catalogVersion": "V1",
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
  "categories": [
    {
      "id": null,
      "categoryId": 1,
      "weightOverride": null,
      "required": false,
      "applicable": true
    }
  ],
  "indicators": [
    {
      "id": null,
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
      "id": null,
      "testCaseId": 1,
      "weightOverride": null,
      "enabled": true
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.scheme.adapter.in.web.EvaluationSchemeRequest` 源码生成 · 2026-08-19*